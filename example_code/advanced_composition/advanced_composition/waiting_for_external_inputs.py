from datetime import timedelta

from flytekit import sleep, task, workflow


@task
def long_running_computation(num: int) -> int:
    """A mock task pretending to be a long-running computation."""
    return num


@workflow
def sleep_wf(num: int) -> int:
    """Simulate a "long-running" computation with sleep."""

    # increase the sleep duration to actually make it long-running
    sleeping = sleep(timedelta(seconds=10))
    result = long_running_computation(num=num)
    sleeping >> result
    return result


# ## Supply external inputs with `wait_for_input`
import typing

from flytekit import wait_for_input


@task
def create_report(data: typing.List[float]) -> dict:  # o0
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


# Continue executions with `approve`
from flytekit import approve


@workflow
def reporting_with_approval_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title", timeout=timedelta(hours=1), expected_type=str)
    final_report = finalize_report(report=report, title=title_input)

    # approve the final report, where the output of approve is the final_report
    # dictionary.
    return approve(final_report, "approve-final-report", timeout=timedelta(hours=2))


# A version of the report-publishing
# workflow where the approval happens after `create_report`
@workflow
def approval_as_promise_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title", timeout=timedelta(hours=1), expected_type=str)

    # wait for report to run so that the user can view it before adding a custom
    # title to the report
    report >> title_input

    final_report = finalize_report(
        report=approve(report, "raw-report-approval", timeout=timedelta(hours=2)),
        title=title_input,
    )
    return final_report


# Working with conditionals
# To illustrate this, let's extend the report-publishing use case so that we
# This example produces an "invalid report" output in case we don't approve the final report:
from flytekit import conditional


@task
def invalid_report() -> dict:
    return {"invalid_report": True}


@workflow
def conditional_wf(data: typing.List[float]) -> dict:
    report = create_report(data=data)
    title_input = wait_for_input("title-input", timeout=timedelta(hours=1), expected_type=str)

    # Define a "review-passes" wait_for_input node so that a human can review
    # the report before finalizing it.
    review_passed = wait_for_input("review-passes", timeout=timedelta(hours=2), expected_type=bool)
    report >> review_passed

    # This conditional returns the finalized report if the review passes,
    # otherwise it returns an invalid report output.
    return (
        conditional("final-report-condition")
        .if_(review_passed.is_true())
        .then(finalize_report(report=report, title=title_input))
        .else_()
        .then(invalid_report())
    )
