import typing

from flytekit import task, workflow


@task
def say_hello() -> str:
    return "hello world"


@workflow
def my_wf() -> str:
    res = say_hello()
    return res


if __name__ == "__main__":
    print(f"Running my_wf() {my_wf()}")

