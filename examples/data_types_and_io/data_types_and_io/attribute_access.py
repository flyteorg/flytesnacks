# %% [markdown]
# (attribute_access)=
#
# # Accessing Attributes
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# You can directly access attributes on output promises for lists, dicts, dataclasses and combinations of these types in Flyte.
# This functionality facilitates the direct passing of output attributes within workflows,
# enhancing the convenience of working with complex data structures.
#
# To begin, import the required dependencies and define a common task for subsequent use.
# %%
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from flytekit import WorkflowFailurePolicy, task, workflow


@task
def print_message(message: str):
    print(message)
    return


# %% [markdown]
# ## List
# You can access an output list using index notation.
#
# :::{important}
# Flyte currently does not support output promise access through list slicing.
# :::
# %%
@task
def list_task() -> list[str]:
    return ["apple", "banana"]


@workflow
def list_wf():
    items = list_task()
    first_item = items[0]
    print_message(message=first_item)


# %% [markdown]
# ## Dictionary
# Access the output dictionary by specifying the key.
# %%
@task
def dict_task() -> dict[str, str]:
    return {"fruit": "banana"}


@workflow
def dict_wf():
    fruit_dict = dict_task()
    print_message(message=fruit_dict["fruit"])


# %% [markdown]
# ## Data class
# Directly access an attribute of a dataclass.
# %%
@dataclass_json
@dataclass
class Fruit:
    name: str


@task
def dataclass_task() -> Fruit:
    return Fruit(name="banana")


@workflow
def dataclass_wf():
    fruit_instance = dataclass_task()
    print_message(message=fruit_instance.name)


# %% [markdown]
# ## Complex type
# Combinations of list, dict and dataclass also work effectively.
# %%
@task
def advance_task() -> (dict[str, list[str]], list[dict[str, str]], dict[str, Fruit]):
    return {"fruits": ["banana"]}, [{"fruit": "banana"}], {"fruit": Fruit(name="banana")}


@task
def print_list(fruits: list[str]):
    print(fruits)


@task
def print_dict(fruit_dict: dict[str, str]):
    print(fruit_dict)


@workflow
def advanced_workflow():
    dictionary_list, list_dict, dict_dataclass = advance_task()
    print_message(message=dictionary_list["fruits"][0])
    print_message(message=list_dict[0]["fruit"])
    print_message(message=dict_dataclass["fruit"].name)

    print_list(fruits=dictionary_list["fruits"])
    print_dict(fruit_dict=list_dict[0])


# %% [markdown]
# You can run all the workflows locally as follows:
# %%
if __name__ == "__main__":
    list_wf()
    dict_wf()
    dataclass_wf()
    advanced_workflow()


# %% [markdown]
# ## Failure scenario
# The following workflow fails because it attempts to access indices and keys that are out of range:
# %%
@task
def failed_task() -> (list[str], dict[str, str], Fruit):
    return ["apple", "banana"], {"fruit": "banana"}, Fruit(name="banana")


@workflow(
    # The workflow remains unaffected if one of the nodes encounters an error, as long as other executable nodes are still available
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE
)
def failed_workflow():
    fruits_list, fruit_dict, fruit_instance = failed_task()
    print_message(message=fruits_list[100])  # Accessing an index that doesn't exist
    print_message(message=fruit_dict["fruits"])  # Accessing a non-existent key
    print_message(message=fruit_instance.fruit)  # Accessing a non-existent param
