import pandas as pd
from flytekit import task, workflow
from flytekit.types.structured.structured_dataset import (
    StructuredDataset,
)


@task
def get_df(a: int) -> pd.DataFrame:
    return pd.DataFrame(
        {"Name": ["Tom", "Joseph"], "Age": [a, 22], "Height": [160, 178]}
    )


@workflow
def basic_wf(a: int) -> pd.DataFrame:
    df = get_df(a=a)
    return df


@task
def show_df(df: pd.DataFrame):
    print(df)


@workflow
def print_wf(df: pd.DataFrame):
    show_df(df=df)
