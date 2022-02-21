"""
Subworkflows 
------------

Subworkflows are similar to :ref:`launch plans <Launch plans>` in that they allow users to kick off one workflow from inside another. 

What's the difference? 
Think of launch plans as pass by pointer and subworkflows as pass by value.

.. note::

    The reason why subworkflows exist is because this is exactly how dynamic workflows are handled by Flyte. So
    instead of hiding this functionality, we expose it at the user level. There are pros and cons of
    using subworkflows as described below.

When Should I Use SubWorkflows?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to limit parallelism within a workflow and its launched sub-flows, subworkflows provide a clean way
to achieve that because they execute within the same context of the parent workflow. 
Thus, all nodes of a subworkflow are constrained to the total constraint on the parent workflow.

Consider this: When you include Workflow A as a subworkflow of Workflow B, and when Workflow B is run, the entire graph of workflow A is simply
copied into workflow B at the point where it is called.

Let's understand subworkflow with an example.
"""

# %%
# Example
# --------
# We import the required dependencies into the environment.
import typing
from typing import Tuple
from flytekit import task, workflow

# %%
# Next, we define a task that uses named outputs.
# We usually try and define ``NamedTuple`` as a distinct type as a best practice (although it can be defined inline).
op = typing.NamedTuple("OutputsBC", t1_int_output=int, c=str)

@task
def t1(a: int) -> op:
    return op(a + 2, "world")

# %%
# Then we define a subworkflow like a typical workflow that can run like any other workflow.
@workflow
def my_subwf(a: int = 42) -> Tuple[str, str]:
    x, y = t1(a=a)
    u, v = t1(a=x)
    return y, v

# %%
# We call the workflow declared above in a `parent` workflow below
# which showcases how to override the node name of a task (or subworkflow in this case). 
# 
# Typically, nodes are just named sequentially: ``n0``, ``n1``, and so on. Since the inner ``my_subwf`` also has a ``n0``, you may
# wish to change the name of the first one. Not changing the name is fine because Flyte automatically prepends an attribute
# to the inner ``n0`` since node IDs must be distinct within a workflow graph. 
@workflow
def parent_wf(a: int) -> Tuple[int, str, str]:
    x, y = t1(a=a).with_overrides(node_name="node-t1-parent")
    u, v = my_subwf(a=x)
    return x, u, v

# %%
# .. note::
#      The with_overrides method provides a new name to the graph-node for better rendering or readability.

# %%
# You can run the subworkflows locally.
if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf(a=3)}")


# %%
# Subworkflows Within a Workflow
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Interestingly, we can nest subworkflows within other subworkflows.
# Workflows can be simply composed from other workflows, even if the other workflows are standalone entities. Each of the
# workflows in this module can exist and run independently.
@workflow
def nested_parent_wf(a: int) -> Tuple[int, str, str, str]:
    x, y = my_subwf(a=a)
    m, n, o = parent_wf(a=a)
    return m, n, o, y


# %%
# You can run the nested workflows locally as well.
if __name__ == "__main__":
    print(f"Running nested_parent_wf(a=3) {nested_parent_wf(a=3)}")


# %%
# External Workflow
# ------------------
#
# When launch plans are used within a workflow to launch the execution of a previously defined workflow, a new
# external execution is launched, with a separate execution ID and can be observed as a distinct entity in
# FlyteConsole/Flytectl. 
#
# They may have separate parallelism constraints since the context is not shared.
# We refer to such external invocations of a workflow using launch plans from a parent workflow as ``External Workflows``.
#
# .. tip::
# 
#    If your deployment uses :ref:`multicluster-setup <Using Multiple Kubernetes Clusters>`, then external workflows may allow you to distribute the workload of a workflow to multiple clusters.
#
# Here is an example demonstrating external workflows:

# %%
import typing
from typing import Tuple
from flytekit import task, workflow
from flytekit import conditional, task, workflow, LaunchPlan

# %%
# We define a task that checks if a string is a palindrome, and returns True if it is one.
@task
def check_palindrome_str(x: str, y: str) -> bool:
    x = y[::-1]
    if x == y :
        result = True
    else:
        result = False
    return result
    
# %%
# We define a workflow that runs the previously defined task.
@workflow
def ext_workflow(my_input1: str, my_input2: str) -> bool:
    result = check_palindrome_str(x=my_input1, y=my_input2)
    return result

# %%
# We create a launch plan which helps kick off one workflow from inside another (in this case). 
my_ext_lp = LaunchPlan.get_or_create(ext_workflow, "parent_workflow_execution",)


# %%
# We define another task that checks if a list of elements forms a palindrome, and returns True if it is one.
@task
def check_palindrome_num(m: typing.List[int], n: typing.List[int]) -> bool:
    m = n[::-1]
    if m == n :
        result = True
    else:
        result = False
    return result

# %%
# We define a workflow which uses the launch plan of the previously defined workflow, which demonstrates external workflow.
@workflow
def parent_workflow(my_input3: typing.List[int], my_input4: typing.List[int]) -> Tuple[bool,bool] :
    my_op1 = my_ext_lp(my_input1 = 'refer', my_input2 = 'refer')
    my_op2 = check_palindrome_num(m = my_input3, n = my_input4)
    return my_op1, my_op2

# %%
# You can run the external workflow locally.
if __name__ == "__main__":
    print("Running parent workflow...")
    print("Checking if both the integer lists and strings are palindromes...")
    print(parent_workflow(my_input3 = [1,2,1], my_input4 =[1,2,1]))