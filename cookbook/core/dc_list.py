from typing import List
from flytekit import task, workflow
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Test:
    x: List[str]

@task
def foo() -> Test:
    return Test(['hi'])

@task
def bar(test: Test) -> Test:
    return Test([x + 'a' for x in test.x])

@workflow
def wf() -> Test:
    foo_out = foo()
    bar_out = bar(test=foo_out)
    return bar_out
