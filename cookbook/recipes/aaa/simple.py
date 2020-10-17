import typing

from flytekit.annotated.task import task
from flytekit.annotated.workflow import workflow


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"


@task
def t2(a: str, b: str) -> str:
    return b + a


@workflow
def my_wf(a: int, b: str) -> (int, str):
    x, y = t1(a=a)
    d = t2(a=y, b=b)
    return x, d
