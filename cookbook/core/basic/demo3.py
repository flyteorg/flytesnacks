import typing

from flytekit import conditional, dynamic, task, workflow

from datetime import datetime
from random import random, seed

# seed random number generator
seed(datetime.now().microsecond)


@task
def native_sort(numbers: typing.List[int]) -> typing.List[int]:
    return sorted(numbers)


@dynamic
def split_and_recurse(numbers: typing.List[int], base_case_limit: int) -> typing.List[int]:
    left = numbers[0:int(len(numbers) / 2)]
    right = numbers[int(len(numbers) / 2):]
    half = int(len(numbers) / 2)  # off by one is okay
    # split1, split2, new_count = split(numbers=numbers)
    sorted1 = merge_sort(
        numbers=left, numbers_count=half, base_case_limit=base_case_limit
    )
    sorted2 = merge_sort(
        numbers=right, numbers_count=half, base_case_limit=base_case_limit
    )
    return merge(sorted_list1=sorted1, sorted_list2=sorted2)


@task
def merge(sorted_list1: typing.List[int], sorted_list2: typing.List[int]) -> typing.List[int]:
    result = []

    # Traverse both array
    while len(sorted_list1) > 0 and len(sorted_list2) > 0:
        if sorted_list1[0] < sorted_list2[0]:
            result.append(sorted_list1.pop(0))
        else:
            result.append(sorted_list2.pop(0))

    result.extend(sorted_list1)
    result.extend(sorted_list2)
    return result


@workflow
def merge_sort(numbers: typing.List[int], numbers_count: int, base_case_limit: int = 5):
    if numbers_count < base_case_limit:
        return native_sort(numbers)
    else:
        return split_and_recurse(numbers=numbers, base_case_limit=base_case_limit)


def generate_inputs(numbers_count: int) -> typing.List[int]:
    generated_list = []
    # generate random numbers between 0-1
    for _ in range(numbers_count):
        value = int(random() * 10000)
        generated_list.append(value)

    return generated_list


# %%
# The entire workflow can be executed locally as follows...
if __name__ == "__main__":
    print(f"Running Merge Sort Locally...")
    count = 20
    x = generate_inputs(count)
    print(x)
    print(merge_sort(numbers=x, numbers_count=count))
