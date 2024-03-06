import typing

import pandas as pd

from flytekit import task, workflow
from flytekit.types.file import FlyteFile


@task()
def print_data_file(input: FlyteFile):
    df = pd.read_csv(input)
    print(df.head())


@workflow
def wf(input: FlyteFile):
    print_data_file(input=input)


@task
def t1():
    return 3 + 2


@workflow
def wf1():
    t1()


if __name__ == '__main__':
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    # result = runner.invoke(cli, "--help")
    result = runner.invoke(pyflyte.main, ["run", "--remote", "test2.py", "wf", "--input", "test.csv"])
    print(result.output)
