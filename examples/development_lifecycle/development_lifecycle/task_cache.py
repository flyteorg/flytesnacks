import time

import pandas

# %% [markdown]
# For any {py:func}`flytekit.task` in Flyte, there is always one required import, which is:
# %%
from flytekit import HashMethod, task, workflow, ImageSpec
from flytekit.core.node_creation import create_node
from typing_extensions import Annotated


image_spec = ImageSpec(
    registry="ghcr.io/flyteorg",
    packages=["pandas"],
)


# Task caching is disabled by default to avoid unintended consequences of
# caching tasks with side effects. To enable caching and control its behavior,
# use the `cache` and `cache_version` parameters when constructing a task.
# `cache` is a switch to enable or disable the cache, and `cache_version`
# pertains to the version of the cache.
# `cache_version` field indicates that the task functionality has changed.
# Bumping the `cache_version` is akin to invalidating the cache.
# You can manually update this version and Flyte caches the next execution
# instead of relying on the old cache.
@task(cache=True, cache_version="1.0", container_image=image_spec)  # noqa: F841
def square(n: int) -> int:
    """
     Parameters:
        n (int): name of the parameter for the task will be derived from the name of the input variable.
                 The type will be automatically deduced to ``Types.Integer``.

    Return:
        int: The label for the output will be automatically assigned, and the type will be deduced from the annotation.

    """
    return n * n


# Caching of Non-flyte Offloaded Objects
# The default behavior displayed by Flyte's memoization feature might not
# match the user intuition. For example, this code makes use of pandas dataframes:
@task(container_image=image_spec)
def foo(a: int, b: str) -> pandas.DataFrame:
    df = pandas.DataFrame(...)
    ...
    return df


@task(cache=True, cache_version="1.0", container_image=image_spec)
def bar(df: pandas.DataFrame) -> int:
    return 1


@workflow
def wf(a: int, b: str):
    df = foo(a=a, b=b)
    v = bar(df=df)  # noqa: F841


# If run twice with the same inputs, one would expect that `bar` would trigger
# a cache hit, but it turns out that's not the case because of how dataframes
# are represented in Flyte.
# However, with release 1.2.0, Flyte provides a new way to control memoization
# behavior of literals. This is done via a `typing.Annotated` call on the task signature.
# For example, in order to cache the result of calls to `bar`,
# you can rewrite the code above like this:
def hash_pandas_dataframe(df: pandas.DataFrame) -> str:
    return str(pandas.util.hash_pandas_object(df))


@task(container_image=image_spec)
def foo_1(  # noqa: F811
    a: int,
    b: str,  # noqa: F821
) -> Annotated[pandas.DataFrame, HashMethod(hash_pandas_dataframe)]:  # noqa: F821  # noqa: F821
    df = pandas.DataFrame(...)  # noqa: F821
    ...
    return df


@task(cache=True, cache_version="1.0", container_image=image_spec)  # noqa: F811
def bar_1(df: pandas.DataFrame) -> int:  # noqa: F811
    return 1


@workflow
def wf_1(a: int, b: str):  # noqa: F811
    df = foo(a=a, b=b)  # noqa: F811
    v = bar(df=df)  # noqa: F841


# How caching of offloaded objects works
# Recall how task input values are taken into account to derive a cache key.
# This is done by turning the literal representation into a string and using
# that string as part of the cache key. In the case of dataframes annotated
# with `HashMethod` we use the hash as the representation of the Literal.
# In other words, the literal hash is used in the cache key.
#
# This feature also works in local execution.
# Here's a complete example of the feature
def hash_pandas_dataframe(df: pandas.DataFrame) -> str:
    return str(pandas.util.hash_pandas_object(df))


@task(container_image=image_spec)
def uncached_data_reading_task() -> Annotated[pandas.DataFrame, HashMethod(hash_pandas_dataframe)]:
    return pandas.DataFrame({"column_1": [1, 2, 3]})


@task(cache=True, cache_version="1.0", container_image=image_spec)
def cached_data_processing_task(df: pandas.DataFrame) -> pandas.DataFrame:
    time.sleep(1)
    return df * 2


@task(container_image=image_spec)
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


if __name__ == "__main__":
    df1 = cached_dataframe_wf()
    print(f"Running cached_dataframe_wf once : {df1}")
