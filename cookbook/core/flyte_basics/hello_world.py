"""

Hello World
------------
This simple workflow calls a task that returns "Hello World" and then just sets that as the final output of the workflow.
"""
import typing

from flytekit import task, workflow, dynamic


# You can change the signature of the workflow to take in an argument like this:
# def say_hello(name: str) -> str:
@task
def say_hello() -> str:
    """
    This is the top of the say_hello comment

    Most stuff.
    Some more stuff. fjdlksfjkl fjklds jsdaflajimwivx;w,aemsa lsoz esa.
    fjdsla lxf,a jidsad.elkfdsafjsad

    #coooooolstuff, #intro #autonomouscars
    """
    return "hello world"


@task(retries=10)
def say_hello_error(a: int) -> str:
    if a == 1:
        print("Raising Error")
        raise RuntimeError("my runtime error")
    if a == 2:
        print("Raising Error")
        raise ValueError("my value error")

    return "hi"


@dynamic(retries=10)
def dynamic_wf(a: int) -> str:
    if a == 1:
        raise RuntimeError("runtime error")
    if a == 2:
        raise ValueError("value error")

    return "hi"


@workflow
def dyn_hello(a: int) -> str:
    return dynamic_wf(a=a)


@dynamic(retries=10)
def dynamic_wf_nested(a: int) -> str:
    return dynamic_wf(a=a)


@workflow
def dyn_hello_nested(a: int) -> str:
    return dynamic_wf_nested(a=a)


@workflow
def my_wf() -> str:
    res = say_hello()
    return res


@workflow
def my_wf_error(a: int) -> str:
    res = say_hello_error(a=a)
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


# %%
# In the next few examples you'll learn more about the core ideas of Flyte, which are tasks, workflows, and launch
# plans.

# %%
# .. run-example-cmds::
