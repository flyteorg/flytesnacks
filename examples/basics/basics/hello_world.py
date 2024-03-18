from flytekit import task, workflow


@task
def say_hello() -> str:
    return "Hello, World!"


@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res


if __name__ == "__main__":
    print(f"Running hello_world_wf() {hello_world_wf()}")
