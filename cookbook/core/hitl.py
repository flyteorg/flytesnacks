import typing
from datetime import timedelta

from flytekit.core.gate import approve, wait_for_input
from flytekit.core.task import task
from flytekit.core.workflow import workflow


@task
def t1(a: int) -> int:
    return a + 5


@task
def t2(a: int) -> int:
    return a + 6


@workflow
def wf(a: int) -> typing.Tuple[int, int]:
    x = t1(a=a)
    s1 = wait_for_input("my-signal-name", timeout=timedelta(hours=1), expected_type=bool)
    s2 = wait_for_input("my-signal-name-2", timeout=timedelta(hours=2), expected_type=int)
    z = t1(a=5)
    y = t2(a=s2)
    x2 = t1(a=5)
    t2(a=approve(x2, "approvetest", timeout=timedelta(hours=1)))
    x >> s1
    s1 >> z

    return y, z
