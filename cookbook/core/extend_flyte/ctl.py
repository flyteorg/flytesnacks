from flyteplayground.flytectl.task import FlyteCtlConfig, FlyteCtlTask
from flytekit import workflow


conf = FlyteCtlConfig(
    admin_endpoint="flyteadmin:81",
    insecure=True,
)


ctl_task = FlyteCtlTask(name="my.test.flytectl.command", task_config=conf)


@workflow
def wf(com: str) -> bool:
    return ctl_task(command=com)
