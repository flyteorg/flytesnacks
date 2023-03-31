import pandas as pd
from flytekit import task, workflow


@task
def say_hello() -> str:
    return "hello world"


@task
def printer(s: str):
    print(s)


@workflow
def hello_world_wf() -> str:
    res = say_hello()
    printer(s=res)
    return res


@task
def make_df() -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})


@task
def show_df(df: pd.DataFrame):
    print(f"Shape of df {df.shape}")


@workflow
def df_wf(a: pd.DataFrame):

    res = make_df()
    show_df(df=res)
