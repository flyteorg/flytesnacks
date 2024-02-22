from flytekit import dynamic, task, workflow


@task
def return_index(character: str) -> int:
    if character.islower():
        return ord(character) - ord("a")
    else:
        return ord(character) - ord("A")


@task
def update_list(freq_list: list[int], list_index: int) -> list[int]:
    freq_list[list_index] += 1
    return freq_list


@task
def derive_count(freq1: list[int], freq2: list[int]) -> int:
    count = 0
    for i in range(26):
        count += min(freq1[i], freq2[i])
    return count


@dynamic
def count_characters(s1: str, s2: str) -> int:
    # s1 and s2 should be accessible

    # Initialize empty lists with 26 slots each, corresponding to every alphabet (lower and upper case)
    freq1 = [0] * 26
    freq2 = [0] * 26

    # Loop through characters in s1
    for i in range(len(s1)):
        # Calculate the index for the current character in the alphabet
        index = return_index(character=s1[i])
        # Update the frequency list for s1
        freq1 = update_list(freq_list=freq1, list_index=index)
        # index and freq1 are not accessible as they are promises

    # looping through the string s2
    for i in range(len(s2)):
        # Calculate the index for the current character in the alphabet
        index = return_index(character=s2[i])
        # Update the frequency list for s2
        freq2 = update_list(freq_list=freq2, list_index=index)
        # index and freq2 are not accessible as they are promises

    # Count the common characters between s1 and s2
    return derive_count(freq1=freq1, freq2=freq2)


@workflow
def dynamic_wf(s1: str, s2: str) -> int:
    return count_characters(s1=s1, s2=s2)


if __name__ == "__main__":
    print(dynamic_wf(s1="Pear", s2="Earth"))


from typing import Tuple

from flytekit import conditional, dynamic, task, workflow


@task
def split(numbers: list[int]) -> Tuple[list[int], list[int], int, int]:
    return (
        numbers[0 : int(len(numbers) / 2)],
        numbers[int(len(numbers) / 2) :],
        int(len(numbers) / 2),
        int(len(numbers)) - int(len(numbers) / 2),
    )


@task
def merge(sorted_list1: list[int], sorted_list2: list[int]) -> list[int]:
    result = []
    while len(sorted_list1) > 0 and len(sorted_list2) > 0:
        # Compare the current element of the first array with the current element of the second array.
        # If the element in the first array is smaller, append it to the result and increment the first array index.
        # Otherwise, do the same with the second array.
        if sorted_list1[0] < sorted_list2[0]:
            result.append(sorted_list1.pop(0))
        else:
            result.append(sorted_list2.pop(0))

    # Extend the result with the remaining elements from both arrays
    result.extend(sorted_list1)
    result.extend(sorted_list2)

    return result


@task
def sort_locally(numbers: list[int]) -> list[int]:
    return sorted(numbers)


@dynamic
def merge_sort_remotely(numbers: list[int], run_local_at_count: int) -> list[int]:
    split1, split2, new_count1, new_count2 = split(numbers=numbers)
    sorted1 = merge_sort(numbers=split1, numbers_count=new_count1, run_local_at_count=run_local_at_count)
    sorted2 = merge_sort(numbers=split2, numbers_count=new_count2, run_local_at_count=run_local_at_count)
    return merge(sorted_list1=sorted1, sorted_list2=sorted2)


@workflow
def merge_sort(numbers: list[int], numbers_count: int, run_local_at_count: int = 5) -> list[int]:
    return (
        conditional("terminal_case")
        .if_(numbers_count <= run_local_at_count)
        .then(sort_locally(numbers=numbers))
        .else_()
        .then(merge_sort_remotely(numbers=numbers, run_local_at_count=run_local_at_count))
    )
