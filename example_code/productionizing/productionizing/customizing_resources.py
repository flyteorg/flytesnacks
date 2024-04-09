import typing

from flytekit import Resources, task, workflow


# Define a task and configure the resources to be allocated to it
@task(
    requests=Resources(cpu="1", mem="100Mi", ephemeral_storage="200Mi"),
    limits=Resources(cpu="2", mem="150Mi", ephemeral_storage="500Mi"),
)
def count_unique_numbers(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# Define a task that computes the square of a number
@task
def square(x: int) -> int:
    return x * x


# Use the tasks decorated with memory and storage hints
# like regular tasks in a workflow
@workflow
def my_workflow(x: typing.List[int]) -> int:
    return square(x=count_unique_numbers(x=x))


# Run the workflow locally
if __name__ == "__main__":
    print(count_unique_numbers(x=[1, 1, 2]))
    print(my_workflow(x=[1, 1, 2]))

# In the example below, we sse the `with_overrides` method
# to override the resources allocated to the tasks dynamically.
import typing  # noqa: E402

from flytekit import Resources, task, workflow  # noqa: E402


# Define a task and configure the resources to be allocated to it
@task(requests=Resources(cpu="1", mem="200Mi"), limits=Resources(cpu="2", mem="350Mi"))
def count_unique_numbers_1(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# Define a task that computes the square of a number
@task
def square_1(x: int) -> int:
    return x * x


# The `with_overrides` method overrides the old resource allocations.
@workflow
def my_pipeline(x: typing.List[int]) -> int:
    return square_1(x=count_unique_numbers_1(x=x)).with_overrides(limits=Resources(cpu="6", mem="500Mi"))


# Run the workflow locally
if __name__ == "__main__":
    print(count_unique_numbers_1(x=[1, 1, 2]))
    print(my_pipeline(x=[1, 1, 2]))
