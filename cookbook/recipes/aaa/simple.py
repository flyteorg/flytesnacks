import typing

from flytekit.annotated.task import task
from flytekit.annotated.workflow import workflow
from flytekit.annotated.launch_plan import LaunchPlan


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"


@task
def t2(a: str, b: str) -> str:
    return b + a


@workflow
def my_wf(a: int, b: str) -> (int, str):
    x, y = t1(a=a)
    d = t2(a=y, b=b)
    return x, d


my_wf_lp = LaunchPlan.create(f"{my_wf.name}_demo_lp", my_wf, default_inputs={'a': 3}, fixed_inputs={'b': 'hello'})


@task
def join_strings(a: typing.List[str]) -> str:
    return " ".join(a)


@workflow
def string_join_wf(a: int, b: str) -> (int, str):
    x, y = t1(a=a)
    d = join_strings(a=[b, y])
    return x, d


@workflow
def my_subwf(a: int) -> (str, str):
    x, y = t1(a=a)
    u, v = t1(a=x)
    return y, v


@workflow
def parent_wf(a: int) -> (int, str, str):
    x, y = t1(a=a).with_overrides(node_name="node-t1-parent")
    u, v = my_subwf(a=x)
    return x, u, v
