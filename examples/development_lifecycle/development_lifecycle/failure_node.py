import typing

from flytekit import WorkflowFailurePolicy, task, workflow
from flytekit.types.error.error import FlyteError


@task
def create_cluster(name: str):
    print(f"Creating cluster: {name}")


# Create a task that will fail during execution
@task
def t1(a: int, b: str):
    print(f"{a} {b}")
    raise ValueError("Fail!")


@task
def delete_cluster(name: str):
    print(f"Deleting cluster {name}")


# Create a task that will be executed if any of the tasks in the workflow fail
@task
def clean_up(name: str, err: typing.Optional[FlyteError] = None):
    print(f"Deleting cluster {name} due to {err}")


# Specify the `on_failure` to a cleanup task.
# This task will be executed if any of the tasks in the workflow fail.
# The input of `clean_up` should be the exact same as the input of the workflow.
@workflow(on_failure=clean_up)
def subwf(name: str):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


# By setting the failure policy to `FAIL_AFTER_EXECUTABLE_NODES_COMPLETE`
# to ensure that the `wf1` is executed even if the subworkflow fails.
# In this case, both parent and child workflows will fail,
# resulting in the `clean_up` task being executed twice.
@workflow(on_failure=clean_up, failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def wf1(name: str = "my_cluster"):
    c = create_cluster(name=name)
    subwf(name="another_cluster")
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow
def clean_up_wf(name: str, err: typing.Optional[FlyteError] = None):
    return clean_up(name=name)


# You can also set the `on_failure` to a workflow.
# This workflow will be executed if any of the tasks in the workflow fail.
@workflow(on_failure=clean_up_wf)
def wf2(name: str = "my_cluster"):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d
