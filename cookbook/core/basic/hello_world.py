"""
Hello World Workflow
--------------------

This simple workflow calls a task that returns "Hello World" and then just sets that as the final output of the workflow.

"""
import typing

from flytekit import task, workflow


@task
def say_hello() -> str:
    return "hello world"


# %%
# You can treat the outputs of a task as you normally would a Python function. Assign the output to two variables
# and use them in subsequent tasks as normal. See :py:func:`flytekit.workflow`
@workflow
def my_wf() -> str:
    res = say_hello()
    return res


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
    print(f"Running my_wf() {my_wf()}")
