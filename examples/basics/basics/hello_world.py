# %% [markdown]
#
# # Hello World
#
#
# ```{tags} Basic
# ```
#
# This simple workflow calls a task that returns "Hello World" and then just sets that as the final output of the workflow.

# %%
from flytekit import task, workflow, ImageSpec

# %% [markdown]

# Defining ImageSpec using `flyteorg/flyte` commit with buildkit, e.g. `flytectl demo start --image=ghcr.io/flyteorg/flyte-sandbox-bundled:sha-<LONG_COMMIT>`

image = ImageSpec(
    name="imagespec",
    registry="localhost:30000",
)


# %% [markdown]
# You can change the signature of the workflow to take in an argument like this:


# %%
@task(container_image=image)
def say_hello() -> str:
    return "hello world"


# %% [markdown]
# You can treat the outputs of a task as you normally would a Python function. Assign the output to two variables
# and use them in subsequent tasks as normal. See {py:func}`flytekit.workflow`
# You can change the signature of the workflow to take in an argument like this:


# %%
@workflow
def my_wf() -> str:
    res = say_hello()
    return res


# %% [markdown]
# Execute the Workflow, simply by invoking it like a function and passing in
# the necessary parameters
#
# ```{note}
#
# One thing to remember, currently we only support `Keyword arguments`. So
# every argument should be passed in the form `arg=value`. Failure to do so
# will result in an error
# ````

# %%
if __name__ == "__main__":
    print(f"Running my_wf() {my_wf()}")


# %% [markdown]
# In the next few examples you'll learn more about the core ideas of Flyte, which are tasks, workflows, and launch
# plans.
