# %% [markdown]
# (chain_flyte_entities)=
#
# # Chaining Flyte Entities
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Flytekit offers a mechanism for chaining Flyte entities using the `>>` operator.
# This is particularly valuable when chaining tasks and subworkflows without the need for data flow between the entities.
#
# ## Tasks
#
# Let's establish a sequence where `t1()` occurs after `t0()`, and `t2()` follows `t1()`.
# %%
from flytekit import task, workflow


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


@workflow
def chain_tasks_wf():
    t2_promise = t2()
    t1_promise = t1()
    t0_promise = t0()

    t0_promise >> t1_promise
    t1_promise >> t2_promise


# %% [markdown]
# (chain_subworkflow)=
# ## Sub workflows
#
# Just like tasks, you can chain {ref}`subworkflows <subworkflow>`.
# %%
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


# %% [markdown]
# To run the provided workflows on the Flyte cluster, use the following commands:
#
# ```
# pyflyte run --remote \
#   https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/advanced_composition/advanced_composition/chain_entities.py \
#   chain_tasks_wf
# ```
#
# ```
# pyflyte run --remote \
#   https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/advanced_composition/advanced_composition/chain_entities.py \
#   chain_workflows_wf
# ```
#
# :::{note}
# Chaining tasks and subworkflows is not supported in local environments.
# Follow the progress of this issue [here](https://github.com/flyteorg/flyte/issues/4080).
# :::
