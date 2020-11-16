import typing

from flytekit import task, workflow
from flytekit.annotated.condition import conditional


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"

@task
def t2(a: str) -> str:
    return a

@workflow
def branches_wf(a: int, b: str) -> (int, str):
    x, y = t1(a=a)
    d = (
        conditional("test1")
            .if_(x == 4)
            .then(t2(a=b))
            .elif_(x >= 5)
            .then(t2(a=y))
            .else_()
            .fail("Unable to choose branch")
    )
    f = conditional("test2").if_(d == "hello").then(t2(a="It is hello")).else_().then(t2(a="Not Hello!"))
    return x, f
