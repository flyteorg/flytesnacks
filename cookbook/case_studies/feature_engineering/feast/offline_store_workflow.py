import feast
from flytekit import task, workflow

@task
def abcdefghijklmnopqrstuvwxyz() -> int:
    return 2

@task
def t1() -> int:
    return 1

@task
def add(a: int, b: int) -> int:
    return a + b

@workflow
def wf1() -> int:
    r1 = abcdefghijklmnopqrstuvwxyz()
    # Load data from
    r2 = t1()
    return add(a=r1, b=r2)

if __name__ == '__main__':
    print(f"{wf1()}")
