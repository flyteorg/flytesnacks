import typing
from flytekit import workflow, dynamic
from flytekit import task


@task
def my_task(i: int) -> int:
    print(f"I am {i}")
    return i + 1


@workflow
def my_large_static_wf() -> typing.List[int]:
    v = []
    for i in range(1000):
        v.append(my_task(i=i))
    return v


@dynamic
def dynamic_tk(x: int) -> typing.List[int]:
    v = []
    for i in range(x):
        v.append(my_task(i=i))
    return v


@workflow
def my_large_dynamic_wf() -> typing.List[int]:
    return dynamic_tk(x=1000)


if __name__ == "__main__":
    print(my_large_static_wf())
    print(my_large_dynamic_wf())
