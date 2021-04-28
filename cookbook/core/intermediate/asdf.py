from flytekit import task, workflow
import typing

nt = typing.NamedTuple("SingleNamedOutput", named1=int)


@task
def t1(a: int) -> nt:
    a = a + 2
    return (a,)


@workflow
def subwf(a: int) -> nt:
    return t1(a=a)


@workflow
def wf(b: int) -> nt:
    out = subwf(a=b)
    return t1(a=out.named1)
