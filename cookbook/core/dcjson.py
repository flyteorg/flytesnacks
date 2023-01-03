from dataclasses import dataclass

from dataclasses_json import dataclass_json
from flytekit import task, workflow


@dataclass_json
@dataclass
class SampleBundle(object):
    max_depth: int = 3
    learning_rate: float = 0.1
    objective: str = "logistic"


@task
def dc_printer(dc_example: SampleBundle):
    print(f"This is the dataclass: {dc_example}")


@workflow
def printer_wf(dc_example: SampleBundle):
    dc_printer(dc_example=dc_example)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(printer_wf())
