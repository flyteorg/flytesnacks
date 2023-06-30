import typing
import pandas as pd
import numpy as np

from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory

df1 = pd.DataFrame({"name": ["Tom", "Joseph"], "age": [20, 22]})

data = {
    'A': np.random.randint(1, 100, size=10),
    'B': np.random.randn(10),
    'C': np.random.choice(['foo', 'bar', 'baz'], size=10),
}

df2 = pd.DataFrame(data)


@task
def t1(a: typing.Any) -> int:
    return a


@task
def print_folder(f: FlyteDirectory, df: pd.DataFrame) -> None:
    print(f"df object is {df}")
    print(f"folder object is {f}")


@workflow
def wf(a: typing.Any = 1, f: FlyteDirectory = "/Users/ytong/temp/data/ddir", df: pd.DataFrame = df1) -> int:
    print_folder(f=f, df=df)
    return t1(a=a)


if __name__ == "__main__":
    wf()
