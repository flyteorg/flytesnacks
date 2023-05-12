import time
import subprocess
from flytekit import task, workflow, Resources
from flytekit.types.directory import FlyteDirectory


@task(requests=Resources(mem="1Gi"), limits=Resources(mem="1Gi"))
def waiter_task(a: int) -> str:
    if a == 0:
        time.sleep(86400)
    else:
        time.sleep(a)
    return "hello world"


@task(requests=Resources(mem="1Gi"), limits=Resources(mem="1Gi"))
def dd_and_upload() -> FlyteDirectory:
    command = ["dd", "if=/dev/random", "of=/root/temp_10GB_file", "bs=1", "count=0", "seek=10G"]
    subprocess.run(command)
    return FlyteDirectory("/root/temp_10GB_file")


@workflow
def waiter(a: int = 0) -> str:
    return waiter_task(a=a)


@workflow
def uploader() -> FlyteDirectory:
    return dd_and_upload()
