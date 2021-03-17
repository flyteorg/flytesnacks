import typing

from flytekit.core.task import task
from flytekit.core.workflow import WorkflowTwo


@task
def t1(a: str) -> str:
    return a + " world"


@task
def t2():
    print("side effect")


@task
def t3(a: typing.List[int]) -> int:
    return sum(a)


wb = WorkflowTwo(name="my.workflow")
wb.add_workflow_input("in1", str)
node = wb.add_entity(t1, a=wb.inputs["in1"])
wb.add_entity(t2)
wb.add_workflow_output("from_n0t1", node.outputs["o0"])
