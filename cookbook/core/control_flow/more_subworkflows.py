import typing

from flytekit import task, workflow


@task
def t1(a: int) -> int:
    return a + 2


@workflow
def leaf_subwf(a: int = 42) -> (int, int):
    x = t1(a=a)
    u = t1(a=x)
    return x, u


@workflow
def middle_subwf() -> (int, int):
    s1, s2 = leaf_subwf


@workflow
def parent_wf(a: int) -> (int, str, str):
    x, y = t1(a=a)
    u, v = my_subwf(a=x)
    return x, u, v


if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf(a=3)}")
