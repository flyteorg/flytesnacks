from datetime import timedelta
from flytekit import task, workflow, approve


@task
def mytask() -> int:
    return 1

@workflow
def simple_workflow(
):
    model_scores = mytask()
    approve(
        upstream_item=model_scores,
        name="model_score_review",
        timeout=timedelta(seconds=300),
    )
