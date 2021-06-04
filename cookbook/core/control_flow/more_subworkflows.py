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
    s1, s2 = leaf_subwf(a=50)
    return s2, s2


@workflow
def parent_wf() -> (int, int, int, int):
    m1, m2 = middle_subwf()
    l1, l2 = leaf_subwf()
    return m1, m2, l1, l2


if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf()}")
