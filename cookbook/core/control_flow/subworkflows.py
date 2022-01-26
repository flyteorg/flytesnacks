"""
Subworkflows
------------

:ref:`divedeep-launchplans <Launch plans>` were introduced in the :ref:`divedeep <Basics>` section of this book. Subworkflows are similar in that they allow users
to kick off one workflow from inside another. What's the difference? Think of launch plans as pass by pointer and
subworkflows as pass by value.
Launch plans were introduced in the Basics section of this book. Subworkflows are similar in that they allow users
to kick off one workflow from inside another. What's the difference? Think of launch plans as passing by pointer and
subworkflows as passing by value.

.. note::

    The reason why subworkflows exist is because this is exactly how dynamic workflows are handled by Flyte. So
    the real reason why subworkflows exist is because this is exactly how dynamic workflows are handled by flyte. So
    instead of hiding the functionality, we expose the functionality at the user level. There are pros and cons of
    using subworkflows as described below

When you include a Launch Plan of Workflow A inside Workflow B, when B gets run, a new workflow execution,
replete with a new workflow execution ID, a new Flyte UI link, gets executed.
When you include a launch plan of workflow A inside workflow B, when B gets run, a new workflow execution,
replete with a new workflow execution ID, a new Flyte UI link, will be run.

When you include Workflow A as a subworkflow of Workflow B, when B gets run, the entire workflow A graph is basically
When you include workflow A as a subworkflow of workflow B, when B gets run, the entire workflow A graph is basically
copied into workflow B at the point where it is called.

When should I use SubWorkflows?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to limit parallelism within a workflow and its launched subworkflows, Subworkflows provide a clean way
to achieve that. This is because they execute within the same context of the parent workflow. Thus all nodes of a subworkflow
to do that. This is because they execute within the same context of the parent workflow. Thus all nodes of a subworkflow
will be constrained to the total constraint on the parent workflow

@ -49,7 +41,6 @@ from flytekit import task, workflow

# %%
# The task here also uses named outputs. Note that we always try and define NamedTuple as a separate type, as a best
# practice (though it can be defined inline).
# practice (though it can be defined inline)
op = typing.NamedTuple("OutputsBC", t1_int_output=int, c=str)

@ -81,7 +72,6 @@ def my_subwf(a: int = 42) -> Tuple[str, str]:
#
# .. note::
#
#    Also note the use of with_overrides to provide a new name to the graph-node for better rendering or readability.
#    Also note the use of with_overrides to provide a new name to the graph-node for better rendering or readability
@workflow
def parent_wf(a: int) -> Tuple[int, str, str]:
@ -91,7 +81,6 @@ def parent_wf(a: int) -> Tuple[int, str, str]:


# %%
# You can execute subworkflows locally.
# You can execute subworkflows locally
if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf(a=3)}")
@ -102,7 +91,6 @@ if __name__ == "__main__":
# ^^^^^^^^^^
# You can also nest subworkflows in other subworkflows as shown in the following example. Also note, how workflows
# can be simply composed from other workflows, even if the other workflows are standalone entities. Each of the
# workflows in this module can exist independently and executed independently.
# workflows in this module can exist independently and executed independently
@workflow
def nested_parent_wf(a: int) -> Tuple[int, str, str, str]:
@ -112,83 +100,6 @@ def nested_parent_wf(a: int) -> Tuple[int, str, str, str]:


# %%
# You can execute the nested workflows locally as well.
# You can execute the nested workflows locally as well
if __name__ == "__main__":
    print(f"Running nested_parent_wf(a=3) {nested_parent_wf(a=3)}")


# %%
# Child Worflow
# ^^^^^^^^^^^^^^
# When using LaunchPlans within a workflow to launch an execution of a previously defined workflow, a new
# external execution is launched, with a separate execution ID and can be observed as a distinct entity in
# FlyteConsole/Flytectl etc. Moreover, the context is not shared, which means they may have separate parallelism constraints.
# We refer to these externalized invocations of a workflow using launch plans from a parent workflow as ``Child Workflows``.

# If your deployment is using :ref:`multicluster-setup <multi-cluster setup>`, then Child workflows may allow you to distribute the workload of a workflow potentially to multiple clusters.

# Here is an example demonstrating child workflows:

import typing
from typing import Tuple
from flytekit import task, workflow
from flytekit import conditional, task, workflow, LaunchPlan

# %%
# We define a task that adds and subtracts two numbers when a condition is fulfilled.
@task
def sum_diff(x: float, y: float) -> float:
    op1 = (x+y)*(x-y)
    return op1

# %%
# We define a task that divides and multiplies two numbers when a condition is fulfilled.
@task
def div_mul(a: float, b: float) -> float:
    op2 = (a/b) * (a*b)
    return op2

# %%
# We define a workflow that executes one of the above defined tasks based on the inputs.
@workflow
def parent_workflow(my_input1: float, my_input2: float) -> float:
    return (
        conditional("sum_diff or div_mul")
            .if_(my_input1 > my_input2)
            .then(sum_diff(x = my_input1 , y = my_input2))
            .else_()
            .then(div_mul(a=my_input1, b=my_input2))
    )

# We create a launch plan that uses the above defined workflow. Notice the default inputs here.
my_parent_lp = LaunchPlan.create(
    "parent_workflow_execution",
    parent_workflow,
    default_inputs={"my_input2": 6.0},
)

print("Output when default input is used : ")
print(my_parent_lp(my_input1 = 2.0)) # 4.0 
print("Output when sum_diff method is called : ")
print(my_parent_lp(my_input1 = 4.0, my_input2 = 2.0)) # 12.0
print("Output when div_mul method is called : ")
print(my_parent_lp(my_input1 = 4.0, my_input2 = 8.0)) # 16.0


# %%
# We define another task that demonstrates the exponent operator.
@task
def exp_demo(x: float, y: float) -> float:
    op1 = (x**y)
    return op1

# %%
# We define a workflow which uses the launch plan of the previously defined workflow.
@workflow
def child_workflow(my_input3: float, my_input4: float) -> Tuple[float, float]:
    my_op1 = my_parent_lp(my_input1 = 4.0)
    my_op2 = exp_demo(x = my_input3, y = my_input4)
    return my_op1,my_op2

print(child_workflow(my_input3 = 3.0, my_input4 = 1.0))