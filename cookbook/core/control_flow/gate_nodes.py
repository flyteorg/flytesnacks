"""
Gate Nodes
----------

*new in Flyte 1.3.0*

There are use cases where we want a workflow execution to pause, only to continue
it when it receives some signal from an external source. Some examples of this
use case would be the following:

1. **Model Deployment**: A hyperparameter-tuning workflow that
   trains ``n`` models, where a human needs to inspect a report before approving
   the model for downstream deployment to some serving layer.
2. **Data Labeling**: A workflow that iterates through an image dataset,
   presenting individual images to a human annotator for them label.
3. **Active Learning**: An `active learning <https://en.wikipedia.org/wiki/Active_learning_(machine_learning)>`__
   workflow that trains a model, shows examples for a human annotator to label
   based which examples it's least/most certain about or would provide the most
   information to the model.

Although all of the examples above are human-in-the-loop processes, gate nodes
are not limited to just these use cases: if you have a Flyte workflow that depends
on an input signal from some external process (👩 human or 🤖 machine) in order
to continue, gate nodes provide a few useful constructs to achieve this.
"""

# %%
# Pause executions with the ``sleep`` gate node
# ==============================================
#
# The simplest case of using gate nodes is when you want your workflow to
# :py:func:`~flytekit.sleep` for some specified amount of time before
# continuing.
#
# Though this type of gate node may not be used often in a production setting,
# you might want to do this, for example, if you want to simulate a delay in
# your workflow to mock out the behavior of some long-running computation.

from datetime import timedelta

from flytekit import task, workflow, sleep


@task
def long_running_computation(num: int) -> int:
    """A mock task pretending to be a long-running computation."""
    return num


@workflow
def sleep_wf(num: int) -> int:
    """Simulate a "long-running" computation with sleep."""

    # increase the sleep duration to actually make it long-running
    sleep_node = sleep(timedelta(seconds=10))
    result = long_running_computation(num=num)
    sleep_node >> result
    return result

# %%
# As you can see above, we define a simple ``add_one`` task and a ``wf_sleep``
# workflow. We first create a ``sleep_node`` then a ``result`` node, then
# order the dependencies such that the workflow sleeps for 10 seconds before
# kicking off the ``result`` computation. Finally, we return the ``result``.
#
# Now that you have a general sense of how this works, let's move on to a
# more powerful gate node construct.
#
# Provide user-defined inputs with ``wait_for_input``
# ===================================================
#
# With the :py:func:`~flytekit.wait_for_input` gate node, you can pause a
# workflow execution that requires some external input signal. For example,
# suppose that you have a workflow that publishes an automated analytics report,
# but before publishing it you want to give it a custom title. You can achieve
# this by defining a ``wait_for_input`` node that takes a ``str`` input and
# finalizes the report:

import typing

from flytekit import wait_for_input


@task
def create_report(data: typing.List[float]) -> dict: # o0
    """A toy report task."""
    return {
        "mean": sum(data) / len(data),
        "length": len(data),
        "max": max(data),
        "min": min(data),
    }

@task
def finalize_report(report: dict, title: str) -> dict:
    return {"title": title, **report}

@workflow
def reporting_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title", timeout=timedelta(hours=1), expected_type=str)
    return finalize_report(report=report, title=title_input)

# %%
# Let's breakdown what's happening in the code above:
#
# - In ``reporting_wf`` we first create the raw ``report``
# - Then, we define a ``title`` gate node that will for a string to be provided
#   through the signaling API, which can be done through the Flyte UI or through
#   ``FlyteRemote`` (more on that later). This node will time out after 1 hour.
# - Finally, we pass the ``title_input`` promise into ``finalize_report``, which
#   attaches the custom title to the report.
#
# As mentioned in the beginning of this page, this construct can be used for
# selecting the best-performing model in cases where there isn't a clear single
# metric to determine the best model, or if you're doing data labeling using
# a Flyte workflow.
#
# Continue executions with ``approve``
# ====================================
#
# Finally, the :py:func:`~flytekit.approve` gate node allows you to wait on
# an explicit approval signal before continuing execution. Going back to our
# report-publishing use case, suppose that we want to block the publishing of
# a report for some reason (e.g. they don't appear to be valid):

# %%
# approve based on a task output
from flytekit import approve


@workflow
def reporting_with_approval_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title", timeout=timedelta(hours=1), expected_type=str)
    final_report = finalize_report(report=report, title=title_input)

    # approve the final report, where the output of approve is the final_report
    # dictionary.
    return approve(final_report, "approve-final-report", timeout=timedelta(hours=2))


# %%
# You can also use the output of the ``approve`` function as a promise, feeding
# it to a subsequent task. Let's create a version of our report-publishing
# workflow where the approval happens after ``create_report``:

@workflow
def approval_as_promise_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title", timeout=timedelta(hours=1), expected_type=str)

    # wait for report to 
    report >> title_input

    final_report = finalize_report(
        report=approve(report, "raw-report-approval", timeout=timedelta(hours=2)),
        title=title_input
    )
    return final_report


# %%
# Gate nodes with conditionals
# ============================
#
# The gate node constructs by themselves are useful, but they become even more
# useful when we combine them with other Flyte constructs, like :ref:`conditionals <conditional>`.
#
# To illustrate this, let's extend the report-publishing use case so that we
# produce and "invalid report" output in case we don't approve the final report:

from flytekit import conditional

@task
def invalid_report() -> dict:
    return {"invalid_report": True}

@workflow
def gate_node_with_conditional_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title", timeout=timedelta(hours=1), expected_type=str)
    final_report = finalize_report(report=report, title=title_input)

    # use wait_for_input instead of approve here such that the type of the
    # approved promise is a boolean, not a dictionary
    review_passed = wait_for_input("review-passes", timeout=timedelta(hours=2), expected_type=bool)
    final_report >> review_passed

    return (
        conditional("final-report-condition")
        .if_(review_passed.is_true())
        .then(final_report)
        .else_()
        .then(invalid_report())
    )

# %%
# On top of the ``approved`` node, which we use in the ``conditional`` to
# determine which branch to execute, we also define a ``disapprove_reason``
# gate node, which will be used as an input to the ``invalid_report`` task.
#
# 
# Sending signals to a gate node with ``FlyteRemote``
# ===================================================
#
# For many cases it's enough to use Flyte UI to provide inputs/approvals on
# gate nodes. However, if you want to use the signalling API to set signals
# for gate nodes, you can use the
# :py:meth:`FlyteRemote.set_signal <flytekit.remote.remote.FlyteRemote.set_signal>`
# method. The example below will allow you to set a value for ``title`` gate node
# In the ``gate_node_with_conditional_wf`` workflow defined above, assuming you have
# it registered in a local Flyte cluster started with
# :ref:`flytectl demo start <getting_started_flyte_cluster>`
#
# .. code-block:: python
#
#    import typing
#    from flytekit.remote.remote import FlyteRemote
#    from flytekit.configuration import Config
#
#    remote = FlyteRemote(
#        Config.for_sandbox(),
#        default_project="flytesnacks",
#        default_domain="development",
#    )
#
#    # first kick off the wotrkflow
#    flyte_workflow = remote.fetch_workflow(
#        name="core.control_flow.gate_nodes.gate_node_with_conditional_wf"
#    )
#    execution = remote.execute(flyte_workflow, inputs={"data": [1.0, 2.0, 3.0, 4.0, 5.0]})
#
#    # get a list of signals available for the execution
#    remote.list_signals(execution.id.name)
# 
#    # set a signal value for the "title" gate node
#    remote.set_signal("title", execution.id.name, "my report")
#
#    # set signal value for the "review-passes" gate node
#    remote.set_signal("review-passes", execution.id.name, True)
