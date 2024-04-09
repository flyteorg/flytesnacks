# Workflows
from flytekit import task, workflow


# Define`slope` and `intercept` tasks to compute the slope and
# intercept of the regression line, respectively
@task
def slope(x: list[int], y: list[int]) -> float:
    sum_xy = sum([x[i] * y[i] for i in range(len(x))])
    sum_x_squared = sum([x[i] ** 2 for i in range(len(x))])
    n = len(x)
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)


@task
def intercept(x: list[int], y: list[int], slope: float) -> float:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    intercept = mean_y - slope * mean_x
    return intercept


# Define a workflow to establish the task dependencies.
# Like tasks, workflows are strongly typed.
@workflow
def simple_wf(x: list[int], y: list[int]) -> float:
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return intercept_value


# Run the workflow by calling it as you would with a Python function
# and providing the necessary inputs.
if __name__ == "__main__":
    print(f"Running simple_wf() {simple_wf(x=[-3, 0, 3], y=[7, 4, -2])}")

# ## Use `partial` to provide default arguments to tasks
# Use the functools.partial function to assign default or
# constant values to the parameters of your tasks
import functools


@workflow
def simple_wf_with_partial(x: list[int], y: list[int]) -> float:
    partial_task = functools.partial(slope, x=x)
    return partial_task(y=y)
