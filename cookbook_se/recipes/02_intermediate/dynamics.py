"""
05: Examples of writing dynamic workflows
------------------------------------------

"""
import typing

from flytekit import dynamic, task, workflow


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


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running sub-wf directly my_subwf(a=3) = {my_subwf(a=3)}")
    print(f"Running my_wf(a=5, b='hello') {my_wf(a=5, b='hello')}")
