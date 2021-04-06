import typing

from datetime import datetime
from random import random, seed


# seed random number generator
seed(datetime.now().microsecond)


def native_sort(numbers: typing.List[int]) -> typing.List[int]:
    return sorted(numbers)


def split(numbers: typing.List[int]) -> (typing.List[int], typing.List[int], int):
    return (
        numbers[0:int(len(numbers)/2)],
        numbers[int(len(numbers)/2):],
        int(len(numbers)/2),
    )


def split_and_recurse(numbers: typing.List[int], base_case_limit: int) -> typing.List[int]:
    split1, split2, new_count = split(numbers=numbers)
    sorted1 = merge_sort(
        numbers=split1, numbers_count=new_count, base_case_limit=base_case_limit
    )
    sorted2 = merge_sort(
        numbers=split2, numbers_count=new_count, base_case_limit=base_case_limit
    )
    return merge(sorted_list1=sorted1, sorted_list2=sorted2)


def merge(
    sorted_list1: typing.List[int], sorted_list2: typing.List[int]
) -> typing.List[int]:
    n1 = len(sorted_list1)
    n2 = len(sorted_list2)
    result = []
    i = 0
    j = 0

    # Traverse both array
    while i < n1 and j < n2:
        # Check if current element of first array is smaller than current element of second array. If yes,
        # store first array element and increment first array index. Otherwise do same with second array
        if sorted_list1[i] < sorted_list2[j]:
            result.append(sorted_list1[i])
            i = i + 1
        else:
            result.append(sorted_list2[j])
            j = j + 1

    # Store remaining elements of first array
    while i < n1:
        result.append(sorted_list1[i])
        i = i + 1

    # Store remaining elements of second array
    while j < n2:
        result.append(sorted_list2[j])
        j = j + 1

    return result


def merge_sort(numbers: typing.List[int], numbers_count: int, base_case_limit: int = 5) -> typing.List[int]:
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


if __name__ == "__main__":
    print(f"Running Merge Sort Locally...")
    count = 20
    x = generate_inputs(count)
    print(x)
    print(merge_sort(numbers=x, numbers_count=count))
