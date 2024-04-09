# Map tasks
from flytekit import map_task, task, workflow


# Example 1
threshold = 11


@task
def detect_anomalies(data_point: int) -> bool:
    return data_point > threshold


@workflow
def map_workflow(data: list[int] = [10, 12, 11, 10, 13, 12, 100, 11, 12, 10]) -> list[bool]:
    # Use the map task to apply the anomaly detection function to each data point
    return map_task(detect_anomalies)(data_point=data)


if __name__ == "__main__":
    print(f"Anomalies Detected: {map_workflow()}")


# Example 2
# When defining a map task, avoid calling other tasks in it. Flyte
# can't accurately register tasks that call other tasks. While Flyte
# will correctly execute a task that calls other tasks, it will not be
# able to give full performance advantages. This is
# especially true for map tasks.
#
# In this example, the map task `suboptimal_mappable_task` would not
# give you the best performance
@task
def upperhalf(a: int) -> int:
    return a / 2 + 1


@task
def suboptimal_mappable_task(a: int) -> str:
    inc = upperhalf(a=a)
    stringified = str(inc)
    return stringified


# Example 3
# Map a task with multiple inputs
@task
def multi_input_task(quantity: int, price: float, shipping: float) -> float:
    return quantity * price * shipping


# Example 4
# Using the `partial` function to partially bind values to the map task
import functools


@workflow
def multiple_inputs_map_workflow(list_q: list[int] = [1, 2, 3, 4, 5], p: float = 6.0, s: float = 7.0) -> list[float]:
    partial_task = functools.partial(multi_input_task, price=p, shipping=s)
    return map_task(partial_task)(quantity=list_q)


# Example 5
# Bind the outputs of a task to partials
@task
def get_price() -> float:
    return 7.0


@workflow
def map_workflow_partial_with_task_output(list_q: list[int] = [1, 2, 3, 4, 5], s: float = 6.0) -> list[float]:
    p = get_price()
    partial_task = functools.partial(multi_input_task, price=p, shipping=s)
    return map_task(partial_task)(quantity=list_q)


# Example 6
# Provide multiple lists as input to a `map_task`
@workflow
def map_workflow_with_lists(
    list_q: list[int] = [1, 2, 3, 4, 5], list_p: list[float] = [6.0, 9.0, 8.7, 6.5, 1.2], s: float = 6.0
) -> list[float]:
    partial_task = functools.partial(multi_input_task, shipping=s)
    return map_task(partial_task)(quantity=list_q, price=list_p)
