from flytekit import LaunchPlan, task, workflow


@task
def t2():
    print("Running t2")
    return


@task
def t1():
    print("Running t1")
    return


@task
def t0():
    print("Running t0")
    return


# Chaining tasks
@workflow
def chain_tasks_wf():
    t2_promise = t2()
    t1_promise = t1()
    t0_promise = t0()

    t0_promise >> t1_promise
    t1_promise >> t2_promise


# Chaining subworkflows
@workflow
def sub_workflow_1():
    t1()


@workflow
def sub_workflow_0():
    t0()


@workflow
def chain_workflows_wf():
    sub_wf1 = sub_workflow_1()
    sub_wf0 = sub_workflow_0()

    sub_wf0 >> sub_wf1


# Chaining launchplans


@workflow
def chain_launchplans_wf():
    lp1 = LaunchPlan.get_or_create(sub_workflow_1, "lp1")()
    lp0 = LaunchPlan.get_or_create(sub_workflow_0, "lp0")()

    lp0 >> lp1
