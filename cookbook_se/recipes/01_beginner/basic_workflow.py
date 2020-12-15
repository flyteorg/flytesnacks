"""
02: Write a simple workflow
------------------------------

Once you've had a handle on tasks, we can move to workflows. Workflow are the other basic building block of Flyte.
Take a look at the conceptual `discussion <https://lyft.github.io/flyte/user/concepts/workflows_nodes.html#workflows>`__
behind workflows for additional information.

"""
import typing

from flytekit import LaunchPlan, task, workflow


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

# %%
# Execute the Workflow, simply by invoking it like a function and passing in
# the necessary parameters
#
# .. note::
#
#   One thing to remember, currently we only support ``Keyword arguments``. So
#   every argument should be passed in the form ``arg=value``. Failure to do so
#   will result in an error
if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf(a=3)}")
    print(
        f"Running parent_wf_with_subwf_default(a=30) {parent_wf_with_subwf_default(a=30)}"
    )
    print(
        f"Running parent_wf_with_lp_with_default(a=40) {parent_wf_with_lp_with_default(a=40)}"
    )
    print(
        f"Running parent_wf_with_lp_overriding_input(a=50) {parent_wf_with_lp_overriding_input(a=50)}"
    )
