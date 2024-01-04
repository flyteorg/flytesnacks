# %% [markdown]
# (failure_node)=
#
# # Failure Node
#
# ```{eval-rst}
# .. tags:: FailureNode, Intermediate
# ```
#
# Failure node is a feature that allows you to specify a node to execute in case of a failure.
# This is useful when you want to execute a cleanup task when certain tasks fail.
#
# To begin, import the necessary dependencies.
# %%
from flytekit import task, workflow, WorkflowFailurePolicy


@task
def create_cluster(name: str):
    print(f"Creating cluster: {name}")


# %% [markdown]
# Create a task that will fail during execution.
# %%
@task
def t1(a: int, b: str):
    print(f"{a} {b}")
    raise ValueError("Fail!")


@task
def delete_cluster(name: str):
    print(f"Deleting cluster {name}")


# %% [markdown]
# Create a task that will be executed if any of the tasks in the workflow fail.
# %%
@task
def clean_up(name: str):
    print(f"Cleaning up cluster {name}")


# %% [markdown]
# Set the `on_failure` parameter to the cleanup task.
# This task will be executed if any of the tasks in the workflow fail.
# :::{important}
# The input of `clean_up` should be the exact same as the input of the workflow.
# :::
# %%
@workflow(on_failure=clean_up)
def subwf(name: str):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


# %% [markdown]
# Set the failure policy to `FAIL_AFTER_EXECUTABLE_NODES_COMPLETE` to ensure that the `wf1` is executed even if the subworkflow fails.
# In this case, both parent and child workflows will fail. The `clean_up` task will be executed twice.
# %%
@workflow(on_failure=clean_up, failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def wf1(name: str = "my_cluster"):
    c = create_cluster(name=name)
    subwf(name="another_cluster")
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow
def clean_up_wf(name: str):
    return clean_up(name=name)


# %% [markdown]
# You can also set the `on_failure` parameter to a workflow.
# This workflow will be executed if any of the tasks in the workflow fail.

# %%
@workflow(on_failure=clean_up_wf)
def wf2(name: str = "my_cluster"):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d
