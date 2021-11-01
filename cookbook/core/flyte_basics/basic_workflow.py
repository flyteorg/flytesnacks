"""
Workflows
----------

Once you've had a handle on tasks, we can move to workflows. Workflow are the other basic building block of Flyte.

Workflows string together two or more tasks. They are also written as Python functions, but it is important to make a
critical distinction between tasks and workflows.

The body of a task's function runs at "run time", i.e. on the K8s cluster (using the task's container), in a Query
Engine, like BigQuery etc, or some other hosted service like AWS Batch, Sagemaker etc. The body of a
workflow is not used for computation, it is only used to structure the tasks, i.e. the output of ``t1`` is an input
of ``t2`` in the workflow below. As such, the body of workflows is run at "registration" time. Please refer to the
registration docs for additional information as well since it is actually a two-step process.

Take a look at the conceptual :std:ref:`discussion <flyte:divedeep-workflow-nodes>`.
behind workflows for additional information.

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


# %%
# You can treat the outputs of a task as you normally would a Python function. Assign the output to two variables
# and use them in subsequent tasks as normal. See :py:func:`flytekit.workflow`
#
# The ``@workflow`` decorator wraps a function, which can be seen as a ``lazily`` evaluated promise. The function is
# is parsed and each function call is deferred. The call itself returns a promise, and hence these promises can be
# passed downstream to other functions, but can not really be accessed in the function body.
# The actual ``evaluation`` (evaluation refers to the execution of a task within the workflow) is deferred to when the
# workflow is actually executed.
# A workflow can be executed locally, this, the evaluation will happen immediately, or the workflow can be executed
# using a CLI/UI etc, which will trigger an evaluation. Thus, even though Flyte workflows decorated with ``@workflow``
# look like python functions, they are actually a python-esque, Domain Specific Language (DSL), which treats the
# ``@task`` decorator specially. When it encounters an ``@task`` decorator, it creates a
# :py:class:`flytekit.core.promise.Promise` object, fulfillment of which will be deferred to actual execution time.
#
# Also refer to :py:func:`flytekit.dynamic`, which allows users to create Flyte workflows dynamically. They defer
# from ``@workflow`` functions, where the actual inputs are pre-materialized, but every invocation of a task still
# results in a promise to be evaluated lazily.
@workflow
def my_wf(a: int, b: str) -> Tuple[int, str]:
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
    print(f"Running my_wf(a=50, b='hello') {my_wf(a=50, b='hello')}")
