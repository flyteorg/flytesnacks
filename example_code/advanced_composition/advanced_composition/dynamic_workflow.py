from flytekit import dynamic, task, workflow

# A workflow whose directed acyclic graph (DAG) is computed at runtime
# is a dynamic workflow.

# Define a task that returns the index of a character,
# where A-Z/a-z is equivalent to 0-25
@task
def return_index(character: str) -> int:
    if character.islower():
        return ord(character) - ord("a")
    else:
        return ord(character) - ord("A")


# Create a task that prepares a list of 26 characters by populating
# the frequency of each character
@task
def update_list(freq_list: list[int], list_index: int) -> list[int]:
    freq_list[list_index] += 1
    return freq_list


# Define a task to calculate the number of common characters
# between the two strings
@task
def derive_count(freq1: list[int], freq2: list[int]) -> int:
    count = 0
    for i in range(26):
        count += min(freq1[i], freq2[i])
    return count


# Define a dynamic workflow to accomplish the following:
#
# 1. Initialize an empty 26-character list to be passed to the `update_list` task
# 2. Iterate through each character of the first string (`s1`) and populate the frequency list
# 3. Iterate through each character of the second string (`s2`) and populate the frequency list
# 4. Determine the number of common characters by comparing the two frequency lists
#
# The looping process is contingent on the number of characters in both strings, which is unknown until runtime
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


# Define a workflow that triggers the dynamic workflow
@workflow
def dynamic_wf(s1: str, s2: str) -> int:
    return count_characters(s1=s1, s2=s2)


# Run the workflow locally
if __name__ == "__main__":
    print(dynamic_wf(s1="Pear", s2="Earth"))
