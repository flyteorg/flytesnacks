"""
Workflows
----------

Once you've had a handle on tasks, we can dive into Flyte workflows. Workflow is the other fundamental building block of Flyte apart from a Flyte task.

Workflows string together two or more tasks. They are also written as Python functions, but it is essential to make a
critical distinction between tasks and workflows.

The body of a task's function runs at "run time", i.e., on a K8s cluster (using the task's container), in a Query
Engine like BigQuery, or some other hosted service like AWS Batch, Sagemaker, etc. The body of a
workflow is not used for computation; it is only used to structure tasks.
As such, the body of a workflow runs at "registration" time, i.e., the workflow unwraps during registration.
Registration refers to uploading the packaged (serialized) code to the Flyte backend, in order to be able to trigger the workflow.
Please refer to the :std:ref:`registration docs <flyte:divedeep-registration>` to understand registration in Flyte.

Now, let's get started with a simple workflow.
"""
import typing

from flytekit import task, workflow
from typing import Tuple


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"


@task
def t2(a: str, b: str) -> str:
    return b + a


@workflow
def my_wf(a: int, b: str) -> Tuple[int, str]:
    x, y = t1(a=a)
    d = t2(a=y, b=b)
    return x, d


# %%
# ``my_wf`` is the Flyte workflow that accepts two inputs and calls two tasks from within it.
#
# How does a Flyte workflow work?
# ===============================
#
# The ``@workflow`` decorator wraps Python functions (Flyte tasks) which can be assumed as ``lazily`` evaluated promises. The functions are
# parsed, and each function call is deferred until the execution time. The function calls return "promises", which can be
# passed downstream to other functions but cannot be accessed within the workflow.
# The actual ``evaluation`` (evaluation refers to the execution of a task within the workflow) happens when the
# workflow executes.
#
# A workflow can be executed locally where the evaluation will happen immediately, or using the CLI, UI, etc., which will trigger an evaluation.
# Although Flyte workflows decorated with ``@workflow`` look like Python functions, they are actually python-esque, Domain Specific Language (DSL) entities 
# that recognize the ``@task`` decorators. When a workflow encounters a ``@task`` decorator, it creates a
# :py:class:`flytekit.core.promise.Promise` object, fulfillment of which will be deferred until the actual execution time.
#
# .. note::
#   Refer to :py:func:`flytekit.dynamic` to create Flyte workflows dynamically. In a dynamic workflow, unlike a simple workflow,
#   the actual inputs are pre-materialized; however, every invocation of a task still
#   results in a promise to be evaluated lazily.


# %%
# Now, we can execute the workflow by invoking it like a function and sending in the required inputs.
#
# .. note::
#
#   Currently we only support ``Keyword arguments``. So
#   every argument should be passed in the form of ``arg=value``. Failure to do so
#   will result in an error.
if __name__ == "__main__":
    print(f"Running my_wf(a=50, b='hello') {my_wf(a=50, b='hello')}")

# %%
# To know more about workflows, take a look at the conceptual :std:ref:`discussion <flyte:divedeep-workflow-nodes>`.
