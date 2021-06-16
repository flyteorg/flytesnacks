"""
Naming the outputs of a task or a workflow
-------------------------------------------
As a default, Flyte names the outputs of a task or a workflow using a standardized convention. All outputs are named
as `o1, o2, o3, ....on` where `o` is the standard prefix and `1,2,..n` is the index position within the return values.

It is also possible to name the outputs of a task or a workflow, so that it may be easier to refer to them, while
debugging or visualizing them in the UI. This is not possible to do natively in Python, so flytekit provides an
alternate way using ``typing.NamedTuple``

The follow example shows how to name outputs of a task and a workflow.
"""
import typing

from flytekit import task, workflow


# %%
# Named outputs can be declared inline as in the following task signature.
#
# .. note::
#
#  Note the name of the NamedTuple really does not matter. The name of the variable and the type matters. We used a
#  a default name like `OP`
#
@task
def say_hello() -> typing.NamedTuple("OP", greet=str):
    return "hello world"


# %%
#  You can also declare the namedtuple ahead of time and then use it in the signature as follows
wf_outputs = typing.NamedTuple("OP2", greet1=str, greet2=str)


# %%
# As shown in this example you can now refer to the declared namedtuple.
# Also as you can see in the workflow, ``say_hello`` returns a tuple, but as with other tuples, you can simply unbox
# it inline. Also the workflow itself returns a tuple. You can also construct the tuple as you return.
@workflow
def my_wf() -> wf_outputs:
    return say_hello(), say_hello()


# %%
# The workflow can be executed as usual
if __name__ == "__main__":
    print(f"Running my_wf() {my_wf()}")
