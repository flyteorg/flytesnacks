from flytekit import task, workflow, dynamic
from flytekit.core.gate import wait_for_input, approve, sleep
import typing
from datetime import timedelta


named_output = typing.NamedTuple("named_output", foo=int, bar=str)


@task
def t1(a: int) -> int:
    return a + 5


@task
def t2(a: int) -> int: # o0
    return a + 6


@task
def t3(a: int) -> named_output:
    return named_output(a, "my string")


@task
def t4(s: str) -> str:
    return s + " t4"

@task
def t5():
    ...


@workflow
def wf(a: int) -> typing.Tuple[int, int, int]:
    x = t1(a=a)
    s1 = wait_for_input("my-signal-name", timeout=timedelta(hours=1), expected_type=bool)
    s2 = wait_for_input("my-signal-name-2", timeout=timedelta(hours=2), expected_type=int)
    z = t1(a=5)
    y = t2(a=s2)
    q = t2(a=approve(y, "approvalfory", timeout=timedelta(hours=2)))
    x >> s1
    s1 >> z

    return y, z, q


@workflow
def wf2(a: int) -> typing.Tuple[int, str]:
    z = t3(a=5)
    # vp = t5()

    r = t2(a=approve(z.foo, "approvalforzfoo", timeout=timedelta(hours=2)))
    # r2 = t2(a=approve(vp, "approvalfory", timeout=timedelta(hours=2)))

    return r, z.bar


@workflow
def wf_sleep() -> int:
    x = sleep(timedelta(seconds=10))
    b = t1(a=1)
    x >> b
    return b


@dynamic
def dyn(a: int) -> typing.Tuple[int, int, int]:
    x = t1(a=a)
    s1 = wait_for_input("my-signal-name", timeout=timedelta(hours=1), expected_type=bool)
    s2 = wait_for_input("my-signal-name-2", timeout=timedelta(hours=2), expected_type=int)
    z = t1(a=5)
    y = t2(a=s2)
    q = t2(a=approve(y, "approvalfory", timeout=timedelta(hours=2)))
    x >> s1
    s1 >> z

    return y, z, q


@workflow
def wf_dyn(a: int) -> typing.Tuple[int, int, int]:
    y, z, q = dyn(a=a)
    return y, z, q