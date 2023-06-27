import typing

from flytekit import task, workflow


@task
def t1(a: typing.Any) -> int:
    return a


@workflow
def wf(a: typing.Any = 1) -> int:
    return t1(a=a)


if __name__ == "__main__":
    wf()
