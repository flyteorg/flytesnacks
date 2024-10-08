import os
import tempfile
from dataclasses import dataclass

import pandas as pd
from flytekit import ImageSpec, task, workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from flytekit.types.structured import StructuredDataset

# NOTE: If you're using Flytekit version below v1.10, you'll need to decorate with `@dataclass_json` using
# `from dataclass_json import dataclass_json` instead of inheriting from Mashumaro's `DataClassJSONMixin`.
# If you're using Flytekit version >= v1.11.1, you don't need to decorate with `@dataclass_json` or
# inherit from Mashumaro's `DataClassJSONMixin`.

image_spec = ImageSpec(
    registry="ghcr.io/flyteorg",
    packages=["pandas", "pyarrow"],
)


# Python types
# Define a `dataclass` with `int`, `str` and `dict` as the data types
@dataclass
class Datum:
    x: int
    y: str
    z: dict[int, str]


# Once declared, a dataclass can be returned as an output or accepted as an input
@task(container_image=image_spec)
def stringify(s: int) -> Datum:
    """
    A dataclass return will be treated as a single complex JSON return.
    """
    return Datum(x=s, y=str(s), z={s: str(s)})


@task(container_image=image_spec)
def add(x: Datum, y: Datum) -> Datum:
    """
    Flytekit automatically converts the provided JSON into a data class.
    If the structures don't match, it triggers a runtime failure.
    """
    x.z.update(y.z)
    return Datum(x=x.x + y.x, y=x.y + y.y, z=x.z)


# Flyte types
@dataclass
class FlyteTypes:
    dataframe: StructuredDataset
    file: FlyteFile
    directory: FlyteDirectory


@task(container_image=image_spec)
def upload_data() -> FlyteTypes:
    """
    Flytekit will upload FlyteFile, FlyteDirectory and StructuredDataset to the blob store,
    such as GCP or S3.
    """
    # 1. StructuredDataset
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})

    # 2. FlyteDirectory
    temp_dir = tempfile.mkdtemp(prefix="flyte-")
    df.to_parquet(temp_dir + "/df.parquet")

    # 3. FlyteFile
    file_path = tempfile.NamedTemporaryFile(delete=False)
    file_path.write(b"Hello, World!")

    fs = FlyteTypes(
        dataframe=StructuredDataset(dataframe=df),
        file=FlyteFile(file_path.name),
        directory=FlyteDirectory(temp_dir),
    )
    return fs


@task(container_image=image_spec)
def download_data(res: FlyteTypes):
    assert pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]}).equals(res.dataframe.open(pd.DataFrame).all())
    f = open(res.file, "r")
    assert f.read() == "Hello, World!"
    assert os.listdir(res.directory) == ["df.parquet"]


# Define a workflow that calls the tasks created above
@workflow
def dataclass_wf(x: int, y: int) -> (Datum, FlyteTypes):
    o1 = add(x=stringify(s=x), y=stringify(s=y))
    o2 = upload_data()
    download_data(res=o2)
    return o1, o2


# Run the workflow locally
if __name__ == "__main__":
    dataclass_wf(x=10, y=20)
