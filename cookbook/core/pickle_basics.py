from flytekit import task, workflow


# %%
# This People is a user defined complex type, which can be used to pass complex data between tasks.
# We will serialize this class to a pickle file and pass it between different tasks.
#
# .. Note::
#
#   Here we can also `turn this object to dataclass <custom_objects.html>`_ to have better performance.
#   We use simple object here for demo purpose.
#   You may have some object that can't turn into a dataclass, e.g. NumPy, Tensor.
class People:
    def __init__(self, name):
        self.name = name


# %%
# Object can be returned as outputs or accepted as inputs
@task
def greet(name: str) -> People:
    return People(name)


@workflow
def welcome(name: str) -> People:
    return greet(name=name)
