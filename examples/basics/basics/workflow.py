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
def simple_wf(x: list[int], y: list[int]) -> float:
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return intercept_value


if __name__ == "__main__":
    print(f"Running simple_wf() {simple_wf(x=[-3, 0, 3], y=[7, 4, -2])}")


import functools


@workflow
def simple_wf_with_partial(x: list[int], y: list[int]) -> float:
    partial_task = functools.partial(slope, x=x)
    return partial_task(y=y)
