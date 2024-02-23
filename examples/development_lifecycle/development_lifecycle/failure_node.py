# %% [markdown]
# (failure_node)=
#
# # Failure Node
#
# ```{eval-rst}
# .. tags:: FailureNode, Intermediate
# ```
#
# The Failure Node feature enables you to designate a specific node to execute in the event of a failure within your workflow.
#
# For example, workflow involves creating a cluster at the beginning, followed by the execution of tasks, and concluding
# with the deletion of the cluster once all tasks are completed. However, if any task within the workflow encounters an error,
# flyte will abort the entire workflow and won’t delete the cluster. This poses a challenge if you still need to clean up the
# cluster even in a task failure.
#
# A failure node can be incorporated into the workflow to address this issue. This ensures that critical actions,
# such as deleting the cluster, are executed even in the event of failures occurring throughout the workflow execution.
#
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
