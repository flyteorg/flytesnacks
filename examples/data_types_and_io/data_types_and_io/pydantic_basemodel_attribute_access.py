from flytekit import ImageSpec, task, workflow
from pydantic import BaseModel

image_spec = ImageSpec(
    registry="ghcr.io/flyteorg",
    packages=["pydantic>2"],
)


@task(container_image=image_spec)
def print_message(message: str):
    print(message)
    return


# Access an output list using index notation
@task(container_image=image_spec)
def list_task() -> list[str]:
    return ["apple", "banana"]


@workflow
def list_wf():
    items = list_task()
    first_item = items[0]
    print_message(message=first_item)


# Access the output dictionary by specifying the key
@task(container_image=image_spec)
def dict_task() -> dict[str, str]:
    return {"fruit": "banana"}


@workflow
def dict_wf():
    fruit_dict = dict_task()
    print_message(message=fruit_dict["fruit"])


# Directly access an attribute of a Pydantic BaseModel
class Fruit(BaseModel):
    name: str


@task(container_image=image_spec)
def basemodel_task() -> Fruit:
    return Fruit(name="banana")


@workflow
def basemodel_wf():
    fruit_instance = basemodel_task()
    print_message(message=fruit_instance.name)


# Combinations of list, dict, and BaseModel also work effectively
@task(container_image=image_spec)
def advance_task() -> (dict[str, list[str]], list[dict[str, str]], dict[str, Fruit]):
    return (
        {"fruits": ["banana"]},
        [{"fruit": "banana"}],
        {"fruit": Fruit(name="banana")},
    )


@task(container_image=image_spec)
def print_list(fruits: list[str]):
    print(fruits)


@task(container_image=image_spec)
def print_dict(fruit_dict: dict[str, str]):
    print(fruit_dict)


@workflow
def advanced_workflow():
    dictionary_list, list_dict, dict_basemodel = advance_task()
    print_message(message=dictionary_list["fruits"][0])
    print_message(message=list_dict[0]["fruit"])
    print_message(message=dict_basemodel["fruit"].name)

    print_list(fruits=dictionary_list["fruits"])
    print_dict(fruit_dict=list_dict[0])


# Run the workflows locally
if __name__ == "__main__":
    list_wf()
    dict_wf()
    basemodel_wf()
    advanced_workflow()
