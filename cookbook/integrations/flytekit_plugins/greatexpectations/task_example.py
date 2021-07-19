from dataclasses import dataclass
from flytekit import task, workflow, kwtypes, Resources
import pandas as pd
import os
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema
import sqlite3
import typing
from flytekitplugins.greatexpectations import BatchRequestConfig, GETask

"""
Simple Task
"""
simple_task_object = GETask(
    name="getask_simple",
    data_source="data",
    inputs=kwtypes(dataset=str),
    expectation_suite="test.demo",
    data_connector="data_example_data_connector",
    data_context="greatexpectations/great_expectations",
)


@task(cache=True, cache_version="1.0", limits=Resources(mem="500Mi"))
def simple_task(csv_file: str) -> int:
    simple_task_object(dataset=csv_file)
    df = pd.read_csv(os.path.join("greatexpectations", "data", csv_file))
    return df.shape[0]


@workflow
def simple_wf(dataset: str = "yellow_tripdata_sample_2019-01.csv") -> int:
    return simple_task(csv_file=dataset)


"""
FlyteFile
"""
file_task_object = GETask(
    name="getask_flytefile",
    data_source="data",
    inputs=kwtypes(dataset=FlyteFile[typing.TypeVar("csv")]),
    expectation_suite="test.demo",
    data_connector="data_flytetype_data_connector",
    local_file_path="/tmp",
    data_context="greatexpectations/great_expectations",
)


@task(cache=True, cache_version="1.0", limits=Resources(mem="500Mi"))
def file_task(
    dataset: FlyteFile[typing.TypeVar("csv")],
) -> int:
    file_task_object.execute(dataset=dataset)
    return len(pd.read_csv(dataset))


@workflow
def file_wf(
    dataset: FlyteFile[
        typing.TypeVar("csv")
    ] = "https://raw.githubusercontent.com/superconductive/ge_tutorials/main/data/yellow_tripdata_sample_2019-01.csv",
) -> int:
    return file_task(dataset=dataset)


"""
FlyteSchema
"""

schema_task_object = GETask(
    name="getask_schema",
    data_source="data",
    inputs=kwtypes(dataset=FlyteSchema),
    expectation_suite="sqlite.movies",
    data_connector="data_flytetype_data_connector",
    local_file_path="/tmp/test.parquet",
    data_context="greatexpectations/great_expectations",
)


@task(cache=True, cache_version="1.0", limits=Resources(mem="500Mi"))
def schema_task(dataset: FlyteSchema) -> typing.List[str]:
    schema_task_object.execute(dataset=dataset)
    return list(dataset.open().all().columns)


@task(cache=True, cache_version="1.0", limits=Resources(mem="500Mi"))
def sql_to_df() -> FlyteSchema:
    con = sqlite3.connect(os.path.join("greatexpectations", "data", "movies.sqlite"))
    df = pd.read_sql_query("SELECT * FROM movies", con)
    con.close()
    return df


@workflow
def schema_wf() -> typing.List[str]:
    df = sql_to_df()
    return schema_task(dataset=df)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print("Simple GE Task...")
    print(simple_wf())
    print("GE Task with FlyteFile...")
    print(
        file_wf(
            dataset="https://raw.githubusercontent.com/superconductive/ge_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
        )
    )
    print("GE Task with FlyteSchema...")
    schema_wf()
