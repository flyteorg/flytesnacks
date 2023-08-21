from flytekit import task, workflow


@task(interruptible=True, retries=0)
def say_hello() -> str:
    import time
    time.sleep(95600)
    return "hello world"


@workflow
def my_wf() -> str:
    res = say_hello()
    return res

