"""
Using Custom Python Objects
----------------------------

Flyte supports passing JSONs between tasks. But, to simplify the usage for the users and introduce type-safety,
flytekit supports passing custom data objects between tasks. Currently only dataclasses that are decorated with
@dataclasses_json are supported.

This example shows how users can serialize custom JSON-compatible dataclasses between successive tasks using the
excellent `dataclasses_json <https://pypi.org/project/dataclasses-json/>`__ library
"""
import os
import tempfile
import typing
from dataclasses import dataclass

import pandas as pd
from dataclasses_json import dataclass_json
from flytekit import task, workflow, kwtypes

# %%
# This Datum is a user defined complex type, which can be used to pass complex data between tasks.
# Moreover, users can also pass this data between different languages and also input through the Flyteconsole as a
# raw JSON.
#
# .. note::
#
#   Only other supported types can be nested in this class, for example it can only contain other ``@dataclass_json``
#   annotated dataclasses if you want to use complex classes. Arbitrary classes will cause a **failure**.
#
# .. note::
#
#   All variables in DataClasses should be **annotated with their type**. Failure to do should will result in an error
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema


@dataclass_json
@dataclass
class Datum(object):
    """
    Example of a simple custom class that is modeled as a dataclass
    """

    x: int
    y: str
    z: typing.Dict[int, str]


# %%
# We can also use any Flyte type in dataclass
@dataclass_json
@dataclass
class Result:
    schema: FlyteSchema
    file: FlyteFile
    directory: FlyteDirectory

# %%
# Once declared, dataclasses can be returned as outputs or accepted as inputs
@task
def stringify(x: int) -> Datum:
    """
    A dataclass return will be regarded as a complex single json return.
    """
    return Datum(x=x, y=str(x), z={x: str(x)})


@task
def add(x: Datum, y: Datum) -> Datum:
    """
    Flytekit will automatically convert the passed in json into a DataClass. If the structures dont match, it will raise
    a runtime failure
    """
    x.z.update(y.z)
    return Datum(x=x.x + y.x, y=x.y + y.y, z=x.z)


@task
def upload_result() -> Result:
    """
    Flytekit will upload the FlyteFile, FlyteDirectory, FlyteSchema to blob store (GCP, S3)
    """
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    temp_dir = tempfile.mkdtemp(prefix="flyte-")

    schema_path = temp_dir + "/schema.parquet"
    df.to_parquet(schema_path)

    file_path = tempfile.NamedTemporaryFile(delete=False)
    file_path.write(b'Hello world!')
    fs = Result(schema=FlyteSchema(temp_dir), file=FlyteFile(file_path.name), directory=FlyteDirectory(temp_dir))
    return fs


@task
def download_result(res: Result):
    """
    Flytekit will lazily load the FlyteSchema. We download the schema only when users invoke open().
    """
    assert pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]}).equals(res.schema.open().all())
    f = open(res.file, "r")
    assert f.read() == 'Hello world!'
    assert os.listdir(res.directory) == ['schema.parquet']


# %%
# Workflow creation remains identical
@workflow
def wf(x: int, y: int) -> (Datum, Result):
    """
    Dataclasses (JSON) can be returned from a workflow as well.
    """
    res = upload_result()
    download_result(res=res)
    return add(x=stringify(x=x), y=stringify(x=y)), res


if __name__ == "__main__":
    """
    This workflow can be run locally. During local execution also, the dataclasses will be marshalled to and from json.
    """
    wf(x=10, y=20)
