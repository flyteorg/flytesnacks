from dataclasses import dataclass

from dataclasses_json import dataclass_json
from flytekit import task, workflow


@task
def print_message(message: str):
    print(message)
    return


# Access an output list using index notation
@task
def list_task() -> list[str]:
    return ["apple", "banana"]


@workflow
def list_wf():
    items = list_task()
    first_item = items[0]
    print_message(message=first_item)


# Access the output dictionary by specifying the key
@task
def dict_task() -> dict[str, str]:
    return {"fruit": "banana"}


@workflow
def dict_wf():
    fruit_dict = dict_task()
    print_message(message=fruit_dict["fruit"])


# Directly access an attribute of a dataclass
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


# Combinations of list, dict and dataclass also work effectively
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


# Run the workflows locally
if __name__ == "__main__":
    list_wf()
    dict_wf()
    dataclass_wf()
    advanced_workflow()
