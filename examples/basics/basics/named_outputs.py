# %% [markdown]
# (named_outputs)=
#
# # Named Outputs
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# By default, Flyte employs a standardized convention to assign names to the outputs of tasks or workflows.
# Each output is sequentially labeled as `o1`, `o2`, `o3`, ... `on`, where `o` serves as the standard prefix,
# and `1`, `2`, ... `n` indicates the positional index within the returned values.
#
# However, Flyte allows the customization of output names for tasks or workflows.
# This customization becomes beneficial when you're returning multiple outputs
# and you wish to assign a distinct name to each of them.
#
# The following example illustrates the process of assigning names to outputs for both a task and a workflow.
#
# To begin, import the required dependencies.
# %%
from typing import NamedTuple

from flytekit import task, workflow

# %% [markdown]
# Define a `NamedTuple` and assign it as an output to a task.
# %%
slope_value = NamedTuple("slope_value", [("slope", float)])


@task
def slope(x: list[int], y: list[int]) -> slope_value:
    sum_xy = sum([x[i] * y[i] for i in range(len(x))])
    sum_x_squared = sum([x[i] ** 2 for i in range(len(x))])
    n = len(x)
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)


# %% [markdown]
# Likewise, assign a `NamedTuple` to the output of `intercept` task.
# %%
intercept_value = NamedTuple("intercept_value", [("intercept", float)])


@task
def intercept(x: list[int], y: list[int], slope: float) -> intercept_value:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    intercept = mean_y - slope * mean_x
    return intercept


# %% [markdown]
# :::{note}
# While it's possible to create `NamedTuple`s directly within the code,
# it's often better to declare them explicitly. This helps prevent potential linting errors in tools like pypy.
#
# ```
# def slope() -> NamedTuple("slope_value", slope=float):
#     pass
# ```
# :::
#
# You can easily unpack the `NamedTuple` outputs directly within a workflow.
# Additionally, you can also have the workflow return a `NamedTuple` as an output.
#
# :::{note}
# Remember that we are extracting individual task execution outputs by dereferencing them.
# This is necessary because `NamedTuple`s function as tuples and require this dereferencing.
# :::
# %%
slope_and_intercept_values = NamedTuple("slope_and_intercept_values", [("slope", float), ("intercept", float)])


@workflow
def simple_wf_with_named_outputs(x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]) -> slope_and_intercept_values:
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value.slope)
    return slope_and_intercept_values(slope=slope_value.slope, intercept=intercept_value.intercept)


# %% [markdown]
# You can run the workflow locally as follows:
# %%
if __name__ == "__main__":
    print(f"Running simple_wf_with_named_outputs() {simple_wf_with_named_outputs()}")
