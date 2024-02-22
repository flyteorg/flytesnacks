from typing import NamedTuple
from flytekit import task, workflow

slope_value = NamedTuple("slope_value", [("slope", float)])


@task
def slope(x: list[int], y: list[int]) -> slope_value:
    sum_xy = sum([x[i] * y[i] for i in range(len(x))])
    sum_x_squared = sum([x[i] ** 2 for i in range(len(x))])
    n = len(x)
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)


intercept_value = NamedTuple("intercept_value", [("intercept", float)])


@task
def intercept(x: list[int], y: list[int], slope: float) -> intercept_value:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    intercept = mean_y - slope * mean_x
    return intercept


slope_and_intercept_values = NamedTuple("slope_and_intercept_values", [("slope", float), ("intercept", float)])


@workflow
def simple_wf_with_named_outputs(x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]) -> slope_and_intercept_values:
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value.slope)
    return slope_and_intercept_values(slope=slope_value.slope, intercept=intercept_value.intercept)


if __name__ == "__main__":
    print(f"Running simple_wf_with_named_outputs() {simple_wf_with_named_outputs()}")
