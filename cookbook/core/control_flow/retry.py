from flytekit import task, workflow
from flytekit.common.exceptions.user import FlyteRecoverableException


@task(retries=2)
def retryer():
    raise FlyteRecoverableException('This task is supposed to fail')


@workflow
def retrys_wf():
    retried_task = retryer()
