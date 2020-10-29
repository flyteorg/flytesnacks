import typing

from flytekit.annotated.task import dynamic, task
from flytekit.annotated.workflow import workflow


@task
def t1(a: int) -> str:
    a = a + 2
    return "world-" + str(a)


@task
def t2(a: str, b: str) -> str:
    return b + a


@dynamic
def my_subwf(a: int) -> (typing.List[str], int):
    s = []
    for i in range(a):
        s.append(t1(a=i))
    return s, 5


@workflow
def my_wf(a: int, b: str) -> (str, typing.List[str], int):
    x = t2(a=b, b=b)
    v, z = my_subwf(a=a)
    return x, v, z
