from __future__ import absolute_import
from __future__ import print_function

from flytekit.sdk.tasks import inputs, outputs, dynamic_task
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Input, Output, workflow

from sample_workflows.formula_2.tasks import inverse_inner_task, inner_task


def manual_assign_name():
    pass


@inputs(task_input_num=Types.Integer)
@inputs(decider=Types.Boolean)
@outputs(out=Types.Integer)
@dynamic_task
def workflow_builder(wf_params, task_input_num, decider, out):
    wf_params.logging.info("Running inner task... yielding a code generated sub workflow")

    input_a = Input(Types.Integer, help="Tell me something")
    if decider:
        node1 = inverse_inner_task(num=input_a)
    else:
        node1 = inner_task(num=input_a)

    MyUnregisteredWorkflow = workflow(
        inputs={
            'a': input_a,
        },
        outputs={
            'ooo': Output(node1.outputs.out, sdk_type=Types.Integer, help='This is an integer output')
        },
        nodes={
            'node_one': node1,
        }
    )

    setattr(MyUnregisteredWorkflow, 'auto_assign_name', manual_assign_name)
    MyUnregisteredWorkflow._platform_valid_name = 'unregistered'

    unregistered_workflow_execution = MyUnregisteredWorkflow(a=task_input_num)

    yield unregistered_workflow_execution
    out.set(unregistered_workflow_execution.outputs.ooo)


@workflow_class
class DynamicWorkflow(object):
    input_a = Input(Types.Integer, default=5, help="Input for inner workflow")
    inverter_input = Input(Types.Boolean, default=False, help="Should invert or not")
    lp_task = workflow_builder(task_input_num=input_a, decider=inverter_input)
    wf_output = Output(lp_task.outputs.out, sdk_type=Types.Integer)
