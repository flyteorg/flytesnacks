import typing
from flytekit import task, workflow, reference_task, map_task
from flytekit.types.file import FlyteFile

@reference_task(
    project="flytesnacks",
    domain="development",
    name="workflows.regd.my_task",
    # version="6SGHp0-m8-94Ysfbh99fXg",
    version="YnldmKeP3_Q3u8vGQeGqwA",
)
def my_task(input: str) -> FlyteFile:
    ...

@task
def prepare_inputs() -> typing.List[str]:
    return ["hello world", "goodbye world"]

@workflow
def run_workflow() -> None:
    inputs = prepare_inputs()
    my_map = map_task(my_task)(input=inputs)
    return None

