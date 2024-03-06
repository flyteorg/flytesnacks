import time

import pandas

from flytekit import HashMethod, task, workflow
from flytekit.core.node_creation import create_node
from typing_extensions import Annotated


@task(cache=True, cache_version="1.0")  # noqa: F841
def square(n: int) -> int:
    return n * n


@task
def foo(a: int, b: str) -> pandas.DataFrame:
    df = pandas.DataFrame(...)
    ...
    return df


@task(cache=True, cache_version="1.0")
def bar(df: pandas.DataFrame) -> int:
    ...


@workflow
def wf(a: int, b: str):
    df = foo(a=a, b=b)
    v = bar(df=df)  # noqa: F841


def hash_pandas_dataframe(df: pandas.DataFrame) -> str:
    return str(pandas.util.hash_pandas_object(df))


@task
def foo_1(  # noqa: F811
    a: int, b: str  # noqa: F821
) -> Annotated[pandas.DataFrame, HashMethod(hash_pandas_dataframe)]:  # noqa: F821  # noqa: F821
    df = pandas.DataFrame(...)  # noqa: F821
    ...
    return df


@task(cache=True, cache_version="1.0")  # noqa: F811
def bar_1(df: pandas.DataFrame) -> int:  # noqa: F811
    ...  # noqa: F811


@workflow
def wf_1(a: int, b: str):  # noqa: F811
    df = foo(a=a, b=b)  # noqa: F811
    v = bar(df=df)  # noqa: F841


def hash_pandas_dataframe(df: pandas.DataFrame) -> str:
    return str(pandas.util.hash_pandas_object(df))


@task
def uncached_data_reading_task() -> Annotated[pandas.DataFrame, HashMethod(hash_pandas_dataframe)]:
    return pandas.DataFrame({"column_1": [1, 2, 3, 9]})


@task(cache=True, cache_version="1.0")
def cached_data_processing_task(df: pandas.DataFrame) -> pandas.DataFrame:
    time.sleep(1)
    return df * 2


@task
def compare_dataframes(df1: pandas.DataFrame, df2: pandas.DataFrame):
    assert df1.equals(df2)


@workflow
def cached_dataframe_wf():
    raw_data = uncached_data_reading_task()

    # Execute `cached_data_processing_task` twice, but force those
    # two executions to happen serially to demonstrate how the second run
    # hits the cache.
    t1_node = create_node(cached_data_processing_task, df=raw_data)
    t2_node = create_node(cached_data_processing_task, df=raw_data)
    t1_node >> t2_node

    # Confirm that the dataframes actually match
    compare_dataframes(df1=t1_node.o0, df2=t2_node.o0)

