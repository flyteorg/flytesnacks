import os
import tempfile
from pathlib import Path
from typing import Type

from flytekit import Blob, BlobMetadata, BlobType, FlyteContext, Literal, LiteralType, Scalar, task, workflow
from flytekit.extend import TypeEngine, TypeTransformer


# Defined type here represents a list of files on the disk. We will refer to it as `MyDataset`
class MyDataset(object):
    """
    ``MyDataset`` is a collection of files. In Flyte, this maps to a multi-part blob or directory.
    """

    def __init__(self, base_dir: str | None = None):
        if base_dir is None:
            self._tmp_dir = tempfile.TemporaryDirectory()
            self._base_dir = self._tmp_dir.name
            self._files = []
        else:
            self._base_dir = base_dir
            self._files = list(Path(base_dir).iterdir())

    @property
    def base_dir(self) -> str:
        return self._base_dir

    @property
    def files(self) -> list[os.PathLike]:
        return self._files

    def new_file(self, name: str) -> os.PathLike:
        new_file = Path(self._base_dir) / name
        self._files.append(new_file)
        return new_file


# %% [markdown]
# `MyDataset` represents a set of files locally. However, when a workflow consists of multiple steps, we want the data to
# flow between different steps. To achieve this, it is necessary to explain how the data will be transformed to
# Flyte's remote references. To do this, we create a new instance of
# `flytekit.extend.TypeTransformer`, for the type `MyDataset` as follows:
class MyDatasetTransformer(TypeTransformer[MyDataset]):
    _TYPE_INFO = BlobType(format="binary", dimensionality=BlobType.BlobDimensionality.MULTIPART)

    def __init__(self):
        super(MyDatasetTransformer, self).__init__(name="mydataset-transform", t=MyDataset)

    def get_literal_type(self, t: Type[MyDataset]) -> LiteralType:
        """
        This is useful to tell the Flytekit type system that ``MyDataset`` actually refers to what corresponding type.
        In this example, we say its of format binary (do not try to introspect) and there is more than one file in it.
        """
        return LiteralType(blob=self._TYPE_INFO)

    def to_literal(
        self,
        ctx: FlyteContext,
        python_val: MyDataset,
        python_type: Type[MyDataset],
        expected: LiteralType,
    ) -> Literal:
        """
        This method is used to convert from the given python type object ``MyDataset`` to the Literal representation.
        """
        # Step 1: Upload all the data into a remote place recommended by Flyte
        remote_dir = ctx.file_access.get_random_remote_directory()
        ctx.file_access.upload_directory(python_val.base_dir, remote_dir)
        # Step 2: Return a pointer to this remote_dir in the form of a Literal
        return Literal(scalar=Scalar(blob=Blob(uri=remote_dir, metadata=BlobMetadata(type=self._TYPE_INFO))))

    def to_python_value(self, ctx: FlyteContext, lv: Literal, expected_python_type: Type[MyDataset]) -> MyDataset:
        """
        In this method, we want to be able to re-hydrate the custom object from Flyte Literal value.
        """
        # Step 1: Download remote data locally
        local_dir = ctx.file_access.get_random_local_directory()
        ctx.file_access.download_directory(lv.scalar.blob.uri, local_dir)
        # Step 2: Create the ``MyDataset`` object
        return MyDataset(base_dir=local_dir)


# Before we can use MyDataset in our tasks, we need to let Flytekit know that `MyDataset` should be considered as a valid type.
# This is done using `flytekit.extend.TypeEngine`'s `register` method.
TypeEngine.register(MyDatasetTransformer())


# The new type should be ready to use! Let us write an example generator and consumer for this new datatype.
@task
def generate() -> MyDataset:
    d = MyDataset()
    for i in range(3):
        fp = d.new_file(f"x{i}")
        with open(fp, "w") as f:
            f.write(f"Contents of file{i}")

    return d


@task
def consume(d: MyDataset) -> str:
    s = ""
    for f in d.files:
        with open(f) as fp:
            s += fp.read()
            s += "\n"
    return s


@workflow
def wf() -> str:
    return consume(d=generate())


# This workflow can be executed and tested locally.
# Flytekit will exercise the entire path even if you run it locally.
if __name__ == "__main__":
    print(wf())
