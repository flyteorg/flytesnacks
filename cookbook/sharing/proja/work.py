from flytekit import LaunchPlan, dynamic, task, workflow


@task
def dummy_task(a: int) -> int:
    return a


@workflow
def wrapper_workflow(a: int) -> int:
    return dummy_task(a=a)


lp = LaunchPlan.get_or_create(wrapper_workflow)


@dynamic
def dynamic_lp(a: int) -> int:
    return lp(a=a)


@workflow
def workflow_parent(a: int) -> int:
    return dynamic_lp(a=a)
