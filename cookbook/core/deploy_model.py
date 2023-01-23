from datetime import timedelta

from flytekit import approve, current_context, sleep, task, workflow
from flytekitplugins.deck.renderer import MarkdownRenderer


@task(disable_deck=False)
def evaluate_model() -> float:  # noqa
    deck = current_context().default_deck
    m = MarkdownRenderer()
    deck.append(
        m.to_html(
            """
    ## Score
    0.72
    """
        )
    )
    return 0.72


@task
def deploy_model(percentage: float) -> bool:
    print(f"Deploying model to {percentage}")
    # Need something to approve on.
    return True


@workflow
def deploy_model_wf():
    score = evaluate_model()
    approve_to_ten = approve(score, "approve-to-ten", timeout=timedelta(hours=1))
    ten = deploy_model(percentage=10.0)
    approve_to_ten >> ten
    approve_to_fifty = approve(ten, "approve-to-fifty", timeout=timedelta(hours=1))
    fifty = deploy_model(percentage=50.0)
    approve_to_fifty >> fifty
    wait = sleep(duration=timedelta(days=2))
    fifty >> wait
    all = deploy_model(percentage=100.0)
    wait >> all
