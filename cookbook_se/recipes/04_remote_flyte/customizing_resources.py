"""
02: Customizing task resources like mem/cpu
--------------------------------------------

One of the reasons why you would want to use a hosted Flyte environment is due to the potential of leveraging CPU, memory and storage resources, far greater than whats available locally.
Flytekit makes it possible to specify these requirements declaratively and close to where the task itself is declared.

"""
import typing
from flytekit import task, workflow


# %%
# In this example the memory required by the function increases as the dataset size increases. For large datasets we may not be able to run locally. Thus we want to provide hints to flyte backend that we want to request for more memory.
# This is done by simply decorating the task with the hints as shown in the follow code sample
#
# .. warning::
#
#    We are working on changing how the cpu-request, memory is configured. This API is likely to change in alpha-3. The changes will be minimal
#
@task(cpu_request="1", memory_request="2048")
def count_unique_numbers(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# %%
# Now lets create a dummy task that squares the number
@task
def square(x: int) -> int:
    return x * x


# %%
# The tasks decorated with memory and storage hints can be used like regular tasks in a workflow, as follows

@workflow
def my_workflow(x: typing.List[int]) -> int:
    return square(x=count_unique_numbers(x=x))


# %%
# The workflow and task can be executed locally
if __name__ == "__main__":
    # %%
    # Execute the task locally
    print(count_unique_numbers(x=[1, 1, 2]))

    # %%
    # Execute the workflow locally
    print(my_workflow(x=[1, 1, 2]))
