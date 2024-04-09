# Subworkflows
from flytekit import task, workflow


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


@workflow
def slope_intercept_wf(x: list[int], y: list[int]) -> (float, float):
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return (slope_value, intercept_value)


@task
def regression_line(val: int, slope_value: float, intercept_value: float) -> float:
    return (slope_value * val) + intercept_value  # y = mx + c


@workflow
def regression_line_wf(val: int = 5, x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]) -> float:
    slope_value, intercept_value = slope_intercept_wf(x=x, y=y)
    return regression_line(val=val, slope_value=slope_value, intercept_value=intercept_value)


# Run the example locally
if __name__ == "__main__":
    print(f"Executing regression_line_wf(): {regression_line_wf()}")


# It's possible to nest a workflow that contains a subworkflow within another workflow.
# Workflows can be constructed from other workflows, even if they function as standalone entities.
# Each workflow in this module has the capability to exist and run independently.
@workflow
def nested_regression_line_wf() -> float:
    return regression_line_wf()


# Run the nested workflow locally
if __name__ == "__main__":
    print(f"Running nested_regression_line_wf(): {nested_regression_line_wf()}")


# External workflow
#
# When launch plans are employed within a workflow to initiate the execution of a pre-defined workflow,
# a new external execution is triggered. This results in a distinct execution ID and can be identified
# as a separate entity.
from flytekit import LaunchPlan

launch_plan = LaunchPlan.get_or_create(
    regression_line_wf, "regression_line_workflow", default_inputs={"val": 7, "x": [-3, 0, 3], "y": [7, 4, -2]}
)


@workflow
def nested_regression_line_lp() -> float:
    # Trigger launch plan from within a workflow
    return launch_plan()


# Run a workflow containing an external workflow locally
if __name__ == "__main__":
    print(f"Running nested_regression_line_lp(): {nested_regression_line_lp}")
