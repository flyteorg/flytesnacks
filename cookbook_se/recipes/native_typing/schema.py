import pandas
from flytekit import task, workflow
from flytekit.types import schema  # noqa: F401


@task
def get_df(a: int) -> pandas.DataFrame:
    return pandas.DataFrame(data={"col1": [a, 2], "col2": [a, 4]})


@task
def add_df(df: pandas.DataFrame) -> pandas.DataFrame:
    return df.append(pandas.DataFrame(data={"col1": [5, 10], "col2": [5, 10]}))


@workflow
def df_wf(a: int) -> pandas.DataFrame:
    df = get_df(a=a)
    return add_df(df=df)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running df_wf(a=42) {df_wf(a=42)}")
