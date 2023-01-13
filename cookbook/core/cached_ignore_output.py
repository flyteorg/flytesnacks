import typing

from flytekit import dynamic, task, workflow
from flytekit.core.base_task import IgnoreOutputs


@task(cache=True, cache_version="0.1")
def t1(x: int) -> str:
    if x == 3:
        raise IgnoreOutputs("got 3")
    return "hello world"


@workflow
def wf_loop() -> typing.List[str]:
    return [t1(x=i) for i in range(5)]
