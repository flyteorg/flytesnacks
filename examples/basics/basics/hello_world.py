# %% [markdown]
#
# # Hello, World!
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Let's write a Flyte {py:func}`~flytekit.workflow` that invokes a
# {py:func}`~flytekit.task` to generate the output "Hello, World!".
#
# Flyte tasks are the core building blocks of larger, more complex workflows.
# Workflows compose multiple tasks – or other workflows –
# into meaningful steps of computation to produce some useful set of outputs or outcomes.
#
# To begin, import `task` and `workflow` from the `flytekit` library.
# %%
from flytekit import task, workflow


# %% [markdown]
# Define a task that produces the string "Hello, World!".
# Simply using the `@task` decorator to annotate the Python function.
# %%
@task
def say_hello() -> str:
    return "Hello, World!"


# %% [markdown]
# You can handle the output of a task in the same way you would with a regular Python function.
# Store the output in a variable and use it as a return value for a Flyte workflow.
# %%
@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res


# %% [markdown]
# Run the workflow by simply calling it like a Python function.
# %%
if __name__ == "__main__":
    print(f"Running hello_world_wf() {hello_world_wf()}")


# %% [markdown]
# Next, let's delve into the specifics of {ref}`tasks <task>`,
# {ref}`workflows <workflow>` and {ref}`launch plans <launch_plan>`.
