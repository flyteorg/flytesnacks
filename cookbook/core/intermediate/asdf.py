from flytekit import task, workflow


@task
def t1(a: int) -> int:
    a = a + 2
    return a


@workflow
def subwf(a: int) -> int:
    return t1(a=a)


@workflow
def wf(b: int) -> int:
    return subwf(a=b)
