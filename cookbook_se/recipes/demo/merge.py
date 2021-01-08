import typing
from datetime import datetime

from flytekit import task, workflow, dynamic
from flytekit.annotated.condition import conditional
from random import seed
from random import random


# seed random number generator
seed(datetime.now().microsecond)


@task
def split(input: typing.List[int]) -> (typing.List[int], typing.List[int], int):
    return input[0:int(len(input) / 2)], input[int(len(input) / 2) + 1:], len(input) / 2


# One sample implementation for merging. In a more real world example, this might merge file streams and only load
# chunks into the memory.
@task
def merge(x: typing.List[int], y: typing.List[int]) -> typing.List[int]:
    n1 = len(x)
    n2 = len(y)
    result = list[int]()
    i = 0
    j = 0

    # Traverse both array
    while i < n1 and j < n2:
        # Check if current element of first array is smaller than current element of second array. If yes,
        # store first array element and increment first array index. Otherwise do same with second array
        if x[i] < y[j]:
            result.append(x[i])
            i = i + 1
        else:
            result.append(y[j])
            j = j + 1

    # Store remaining elements of first array
    while i < n1:
        result.append(x[i])
        i = i + 1

    # Store remaining elements of second array
    while j < n2:
        result.append(y[j])
        j = j + 1

    return result


# This runs the sorting completely locally. It's faster and more efficient to do so if the entire list fits in memory.
@task
def merge_sort_locally(input: typing.List[int]) -> typing.List[int]:
    return sorted(input)


@dynamic
def merge_sort_remotely(input: typing.List[int]) -> typing.List[int]:
    x, y, new_count = split(input=input)
    sorted_x = merge_sort(input=x, count=new_count)
    sorted_y = merge_sort(input=y, count=new_count)
    return merge(x=sorted_x, y=sorted_y)


@workflow
def merge_sort(input: typing.List[int], count: int) -> typing.List[int]:
    return (
        conditional("terminal_case")
            .if_(count < 1000)
            .then(merge_sort_locally(input=input))
            .else_()
            .then(merge_sort_remotely(input=input))
    )


def generate_inputs(count: int) -> typing.List[int]:
    x = list[int]()
    # generate random numbers between 0-1
    for _ in range(count):
        value = int(random()*10000)
        x.append(value)

    return x


# %%
# The entire workflow can be executed locally as follows...
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(merge_sort(input=generate_inputs(2000), count=2000))