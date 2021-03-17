import typing
from collections import OrderedDict

from flytekit.common.translator import get_serializable
from flytekit.core import context_manager
from flytekit.core.context_manager import Image, ImageConfig
from flytekit.core.launch_plan import LaunchPlan
from flytekit.core.task import task
from flytekit.core.workflow import WorkflowTwo, workflow

default_img = Image(name="default", fqn="test", tag="tag")
serialization_settings = context_manager.SerializationSettings(
    project="project",
    domain="domain",
    version="version",
    env=None,
    image_config=ImageConfig(default_image=default_img, images=[default_img]),
)


def test_wf2():
    @task
    def t1(a: str) -> str:
        return a + " world"

    @task
    def t2():
        print("side effect")

    wb = WorkflowTwo(name="my.workflow")
    wb.add_workflow_input("in1", str)
    node = wb.add_entity(t1, a=wb.inputs["in1"])
    wb.add_entity(t2)
    wb.add_workflow_output("from_n0t1", node.outputs["o0"])

    assert wb(in1="hello") == "hello world"

    srz_wf = get_serializable(OrderedDict(), serialization_settings, wb)
    assert len(srz_wf.nodes) == 2
    assert srz_wf.nodes[0].task_node is not None
    assert len(srz_wf.outputs) == 1
    assert srz_wf.outputs[0].var == "from_n0t1"
    assert len(srz_wf.interface.inputs) == 1
    assert len(srz_wf.interface.outputs) == 1

    # Create launch plan from wf, that can also be serialized.
    lp = LaunchPlan.create("test_wb", wb)
    srz_lp = get_serializable(OrderedDict(), serialization_settings, lp)
    assert srz_lp.workflow_id.name == "my.workflow"


def test_wf2_list_bound():
    @task
    def t1(a: typing.List[int]) -> int:
        return sum(a)

    wb = WorkflowTwo(name="my.workflow.a")
    wb.add_workflow_input("in1", int)
    wb.add_workflow_input("in2", int)
    node = wb.add_entity(t1, a=[wb.inputs["in1"], wb.inputs["in2"]])
    wb.add_workflow_output("from_n0t1", node.outputs["o0"])

    assert wb(in1=3, in2=4) == 7
