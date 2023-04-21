import typing
from flytekit import task, map_task, workflow
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class DataclassA:
    a: str
    b: int
    c: float
    d: float
    e: str
    f: int
    g: bool
    h: int


@task
def prepare_map_inputs() -> typing.List[int]:
    return [1]


@task
def fetch_provider(in1: DataclassA) -> int:
    return i


@workflow
def wf():
    # Prepare inputs for fetch_provider
    prepared = prepare_map_inputs()

    # Run one instance of fetch_provider per provider
    map_task(fetch_provider)(in1=prepared)


