import os
import tempfile

import pandas as pd
from flytekit import ImageSpec, task, workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from flytekit.types.structured import StructuredDataset
from pydantic import BaseModel

image_spec = ImageSpec(
    registry="ghcr.io/flyteorg",
    packages=["pandas", "pyarrow", "pydantic"],
)


# Python types
# Define a Pydantic model with `int`, `str`, and `dict` as the data types
class Datum(BaseModel):
    x: int
    y: str
    z: dict[int, str]


# Once declared, a Pydantic model can be returned as an output or accepted as an input
@task(container_image=image_spec)
def stringify(s: int) -> Datum:
    """
    A Pydantic model return will be treated as a single complex JSON return.
    """
    return Datum(x=s, y=str(s), z={s: str(s)})


@task(container_image=image_spec)
def add(x: Datum, y: Datum) -> Datum:
    """
    Flytekit automatically converts the provided JSON into a Pydantic model.
    If the structures don't match, it triggers a runtime failure.
    """
    x.z.update(y.z)
    return Datum(x=x.x + y.x, y=x.y + y.y, z=x.z)


# Flyte types
class FlyteTypes(BaseModel):
    dataframe: StructuredDataset
    file: FlyteFile
    directory: FlyteDirectory


@task(container_image=image_spec)
def upload_data() -> FlyteTypes:
    """
    Flytekit will upload FlyteFile, FlyteDirectory, and StructuredDataset to the blob store,
    such as GCP or S3.
    """
    # 1. StructuredDataset
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})

    # 2. FlyteDirectory
    temp_dir = tempfile.mkdtemp(prefix="flyte-")
    df.to_parquet(os.path.join(temp_dir, "df.parquet"))

    # 3. FlyteFile
    file_path = tempfile.NamedTemporaryFile(delete=False)
    file_path.write(b"Hello, World!")
    file_path.close()

    fs = FlyteTypes(
        dataframe=StructuredDataset(dataframe=df),
        file=FlyteFile(file_path.name),
        directory=FlyteDirectory(temp_dir),
    )
    return fs


@task(container_image=image_spec)
def download_data(res: FlyteTypes):
    expected_df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    actual_df = res.dataframe.open(pd.DataFrame).all()
    assert expected_df.equals(actual_df), "DataFrames do not match!"

    with open(res.file, "r") as f:
        assert f.read() == "Hello, World!", "File contents do not match!"

    assert os.listdir(res.directory) == ["df.parquet"], "Directory contents do not match!"


# Define a workflow that calls the tasks created above
@workflow
def basemodel_wf(x: int, y: int) -> (Datum, FlyteTypes):
    o1 = add(x=stringify(s=x), y=stringify(s=y))
    o2 = upload_data()
    download_data(res=o2)
    return o1, o2


# Run the workflow locally
if __name__ == "__main__":
    result = basemodel_wf(x=10, y=20)
    print(result)
