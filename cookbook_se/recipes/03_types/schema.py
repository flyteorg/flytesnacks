"""
This example explains how an untyped schema is passed between tasks using pandas.DataFrame.

Flytekit allows users to directly use pandas.dataframe in their tasks as long as they import
.. code:: python

    from flytekit.types import schema # noqa: F401

Note: # noqa: F401. This is to ignore pylint comparing about unused imports
"""
import pandas
from flytekit import task, workflow
from flytekit.types import schema  # noqa: F401


@task
def get_df(a: int) -> pandas.DataFrame:
    """
    Generate a sample dataframe
    """
    return pandas.DataFrame(data={"col1": [a, 2], "col2": [a, 4]})


@task
def add_df(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Append some data to the dataframe.
    NOTE: this may result in runtime failures if the columns do not match
    """
    return df.append(pandas.DataFrame(data={"col1": [5, 10], "col2": [5, 10]}))


@workflow
def df_wf(a: int) -> pandas.DataFrame:
    """
    Pass data between the dataframes
    """
    df = get_df(a=a)
    return add_df(df=df)


if __name__ == "__main__":
    """
    Run this locally
    """
    print(f"Running {__file__} main...")
    print(f"Running df_wf(a=42) {df_wf(a=42)}")
