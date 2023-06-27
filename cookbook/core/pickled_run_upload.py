import typing

from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory


@task
def t1(a: typing.Any) -> int:
    return a


@task
def print_folder(f: FlyteDirectory) -> None:
    print(f"folder object is {f}")


@workflow
def wf(a: typing.Any = 1, f: FlyteDirectory = "/Users/ytong/temp/data/ddir") -> int:
    print_folder(f=f)
    return t1(a=a)


if __name__ == "__main__":
    wf()
