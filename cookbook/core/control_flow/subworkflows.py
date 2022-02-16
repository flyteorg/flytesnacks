"""
Subworkflows and External Workflows
------------------------------------

Subworkflows are similar to :ref:`launch plans <Launch plans>` in that they allow users to kick off one workflow from inside another. 

What's the difference? 
Think of launch plans as pass by pointer and subworkflows as pass by value.

.. note::

    The reason why subworkflows exist is because this is exactly how dynamic workflows are handled by Flyte. So
    instead of hiding this functionality, we expose it at the user level. There are pros and cons of
    using subworkflows as described below.

When you include Workflow A as a subworkflow of Workflow B, and when Workflow B is run, the entire graph of workflow A is simply
copied into workflow B at the point where it is called.

When Should I Use SubWorkflows?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to limit parallelism within a workflow and its launched subworkflows, subworkflows provide a clean way
to achieve that. This is because they execute within the same context of the parent workflow. 
Thus, all nodes of a subworkflow are constrained to the total constraint on the parent workflow.

Let's understand subworkflow with an example:
"""

# %%
# We import the required dependencies into the environment.
import typing
from typing import Tuple
from flytekit import task, workflow

# %%
# The task here uses named outputs. Note that we always try and define NamedTuple as a separate type, as a best
# practice (although it can be defined inline).
op = typing.NamedTuple("OutputsBC", t1_int_output=int, c=str)

@task
def t1(a: int) -> op:
    return op(a + 2, "world")

# %%
# This will be the subworkflow of our examples, but note that this is a workflow like any other. It can be run just
# like any other workflow. Note here that the workflow has been declared with a default.
@workflow
def my_subwf(a: int = 42) -> Tuple[str, str]:
    x, y = t1(a=a)
    u, v = t1(a=x)
    return y, v

# %%
# We call the workflow declared above in the parent workflow below. 
# It showcases how to override the node name of a task (or subworkflow). Typically, nodes are just named
# sequentially, ``n0``, ``n1``, and so on. Because the inner ``my_subwf`` also has a ``n0`` you may
# wish to change the name of the first one. Not doing so is also fine - Flyte automatically prepends an attribute
# to the inner ``n0``, since node IDs need to be distinct within a workflow graph. This issue does not exist
# when calling entities by launch plan since they create a separate execution entirely.
#
# .. note::
#
#     The with_overrides method provides a new name to the graph-node for better rendering or readability.
@workflow
def parent_wf(a: int) -> Tuple[int, str, str]:
    x, y = t1(a=a).with_overrides(node_name="node-t1-parent")
    u, v = my_subwf(a=x)
    return x, u, v


# %%
# You can execute subworkflows locally.
if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf(a=3)}")


# %%
# Nest Subworkflows in Other Workflows
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# You can also nest subworkflows in other subworkflows as shown in the following example. Also note that workflows
# can be simply composed from other workflows, even if the other workflows are standalone entities. Each of the
# workflows in this module can exist and be executed independently.
@workflow
def nested_parent_wf(a: int) -> Tuple[int, str, str, str]:
    x, y = my_subwf(a=a)
    m, n, o = parent_wf(a=a)
    return m, n, o, y


# %%
# You can execute the nested workflows locally as well.
if __name__ == "__main__":
    print(f"Running nested_parent_wf(a=3) {nested_parent_wf(a=3)}")


# %%
# External Workflow
# -----------------
#
# When launch plans are used within a workflow to launch an execution of a previously defined workflow, a new
# external execution is launched, with a separate execution ID and can be observed as a distinct entity in
# FlyteConsole/FlyteCTL etc. 
#
# Moreover, the context is not shared, which means they may have separate parallelism constraints.
# We refer to these externalized invocations of a workflow using launch plans from a parent workflow as ``External Workflows``.
#
# If your deployment uses :ref:`multicluster-setup <Using Multiple Kubernetes Clusters>`, then external workflows may allow you to distribute the workload of a workflow to multiple clusters.
# Here is an example demonstrating external workflows:

# %%
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
def ext_workflow(my_input1: float, my_input2: float) -> float:
    return (
        conditional("sum_diff or div_mul")
            .if_(my_input1 > my_input2)
            .then(sum_diff(x = my_input1 , y = my_input2))
            .else_()
            .then(div_mul(a=my_input1, b=my_input2))
    )

# We create a launch plan that uses the above defined workflow. Notice the default inputs here.
my_ext_lp = LaunchPlan.create(
    "ext_workflow_execution",
    ext_workflow,
    default_inputs={"my_input2": 6.0},
)

# Different input values passed to the above defined function.
print("Output when default input is used : ")
print(my_ext_lp(my_input1 = 2.0)) # 4.0 
print("Output when sum_diff method is called : ")
print(my_ext_lp(my_input1 = 4.0, my_input2 = 2.0)) # 12.0
print("Output when div_mul method is called : ")
print(my_ext_lp(my_input1 = 4.0, my_input2 = 8.0)) # 16.0


# %%
# We define another task that demonstrates the exponent operator.
@task
def exp_demo(x: float, y: float) -> float:
    op1 = (x**y)
    return op1

# %%
# We define a workflow which uses the launch plan of the previously defined workflow, which demonstrates external workflow.
@workflow
def parent_workflow(my_input3: float, my_input4: float) -> Tuple[float, float]:
    my_op1 = my_ext_lp(my_input1 = 4.0)
    my_op2 = exp_demo(x = my_input3, y = my_input4)
    return my_op1,my_op2

# %%
# You can execute the nested workflows locally as well.
if __name__ == "__main__":
    print("Running parent workflow...")
    print(parent_workflow(my_input3 = 3.0, my_input4 = 1.0))