# %% [markdown]
# (chain_flyte_entities)=
#
# # Chain Flyte Entities
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# flytekit provides a mechanism to chain Flyte entities using the `>>` operator.
#
# ## Tasks
#
# Let's enforce an order for `t1()` to happen after `t0()`, and for `t2()` to happen after `t1()`.
#
# Import the necessary dependencies.
# %%
from flytekit import task, workflow


@task
def t2():
    pass


@task
def t1():
    pass


@task
def t0():
    pass


# %% [markdown]
# We want to enforce an order here: `t0()` followed by `t1()` followed by `t2()`.
# %%
@workflow
def chain_tasks_wf():
    t2_promise = t2()
    t1_promise = t1()
    t0_promise = t0()

    t0_promise >> t1_promise
    t1_promise >> t2_promise


# %% [markdown]
# ## Chain SubWorkflows
#
# Similar to tasks, you can chain {ref}`subworkflows <subworkflows>`.
# %%
@workflow
def sub_workflow_1():
    t1()


@workflow
def sub_workflow_0():
    t0()


# %% [markdown]
# Use `>>` to chain the subworkflows.
# %%
@workflow
def chain_workflows_wf():
    sub_wf1 = sub_workflow_1()
    sub_wf0 = sub_workflow_0()

    sub_wf0 >> sub_wf1


# %% [markdown]
# Run the workflows locally.
#
# %%
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running chain_tasks_wf()... {chain_tasks_wf()}")
    print(f"Running chain_workflows_wf()... {chain_workflows_wf()}")
