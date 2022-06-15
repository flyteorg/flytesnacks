"""
Customizing Task Resources
---------------------------

One of the reasons to use a hosted Flyte environment is the potential of leveraging CPU, memory and storage resources, far greater than what's available locally.
Flytekit makes it possible to specify these requirements declaratively and close to where the task itself is declared.

"""

# %%
# In this example, the memory required by the function increases as the dataset size increases.
# Large datasets may not be able to run locally, so we would want to provide hints to flyte backend to request for more memory.
# This is done by simply decorating the task with the hints as shown in the following code sample.
#
# Tasks can have ``requests`` and ``limits`` which mirror the native `equivalents in kubernetes <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits>`__
# A task can possibly be allocated more resources than it requests, but never more than its limit.
# Requests are treated as hints which are used to schedule tasks on nodes with available resources, whereas limits
# are hard constraints.
#
# For either a request or limit, refer to the :py:class:`flytekit:flytekit.Resources` documentation.
#
# The following attributes can be specified for a ``Resource``.
#
# #. ``cpu``
# #. ``mem``
# #. ``gpu``
#
# To ensure regular tasks that don't require GPUs are not scheduled on GPU nodes, a separate node group for GPU nodes can be configured with `taints <https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/>`_.
#
# To ensure tasks that require GPUs get the needed tolerations on their pods, set up FlytePropeller using the following `configuration <https://github.com/flyteorg/flytepropeller/blob/v0.10.5/config.yaml#L51,L56>`_. Ensure that this toleration config matches the taint config you have configured to protect your gpu providing nodes from dealing with regular non-gpu workloads (pods).
#
# The ``storage`` resources option is not yet supported, but coming soon.
#
# The actual values follow the `Kubernetes convention <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes>`_.
# Let's dive into an example.

# %%
# Import the dependencies.
import typing

from flytekit import Resources, task, workflow

# Define a task that returns the count of unique numbers. Specify the resources (such as CPU and memory). 
@task(requests=Resources(cpu="1", mem="100Mi"), limits=Resources(cpu="2", mem="150Mi"))
def count_unique_numbers(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# %%
# Define a task that computes the square of a number.
@task
def square(x: int) -> int:
    return x * x


# %%
# The tasks decorated with memory and storage hints are used like regular tasks in a workflow.
@workflow
def my_workflow(x: typing.List[int]) -> int:
    return square(x=count_unique_numbers(x=x))


# %%
# You can execute the workflow locally.
if __name__ == "__main__":
    print(count_unique_numbers(x=[1, 1, 2]))
    print(my_workflow(x=[1, 1, 2]))

# %%
# Using ``with_overrides`` Method
#
# The ``with_overrides`` method is used to override the resources in the tasks based on the inputs.
# Let's understand it with an example
#

# %%
# Import the dependencies.
from flytekit import task, workflow, Resources

# %%
# Define a task that returns an integer and a string.
@task
def t1(a:int, b:str) -> (int, str):
    return (a,b)

# %%
# Define a task that returns sum of two integers.
@task
def t2(c:int, d:int) -> int:
    return c+d

# %%
# Define a workflow. 
@workflow
def pipeline(a:int, b:str, c:int, d:int) -> int:
    # ``with_overrides`` is used to specify the memory
    op1,op2 = t1(a=a, b=b).with_overrides(limits=Resources(mem="200Mi"))
    op3 = t2(c=op1, d=d)
    return op3

# %%
# You can run the file locally.
if __name__ == "__main__":
    print(f"The output is {pipeline(a=1, b='Joe', c=100, d=10)}")   
    