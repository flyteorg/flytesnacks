# Notifications

from datetime import timedelta
from flytekit import Email, FixedRate, LaunchPlan, PagerDuty, Slack, WorkflowExecutionPhase, task, workflow


@task
def double_int_and_print(a: int) -> str:
    return str(a * 2)


@workflow
def int_doubler_wf(a: int) -> str:
    doubled = double_int_and_print(a=a)
    return doubled


# Here are three scenarios that can help deepen your understanding of how notifications work:
#
# 1. Launch Plan triggers email notifications when the workflow execution reaches the `SUCCEEDED` phase.
int_doubler_wf_lp = LaunchPlan.get_or_create(
    name="email_notifications_lp",
    workflow=int_doubler_wf,
    default_inputs={"a": 4},
    notifications=[
        Email(
            phases=[WorkflowExecutionPhase.SUCCEEDED],
            recipients_email=["admin@example.com"],
        )
    ],
)

# 2. Notifications shine when used for scheduled workflows to alert for failures.
int_doubler_wf_scheduled_lp = LaunchPlan.get_or_create(
    name="int_doubler_wf_scheduled",
    workflow=int_doubler_wf,
    default_inputs={"a": 4},
    notifications=[
        PagerDuty(
            phases=[WorkflowExecutionPhase.FAILED, WorkflowExecutionPhase.TIMED_OUT],
            recipients_email=["abc@pagerduty.com"],
        )
    ],
    schedule=FixedRate(duration=timedelta(days=1)),
)


# 3. Notifications can be combined with different permutations of terminal phases and recipient targets.
wacky_int_doubler_lp = LaunchPlan.get_or_create(
    name="wacky_int_doubler",
    workflow=int_doubler_wf,
    default_inputs={"a": 4},
    notifications=[
        Email(
            phases=[WorkflowExecutionPhase.FAILED],
            recipients_email=["me@example.com", "you@example.com"],
        ),
        Email(
            phases=[WorkflowExecutionPhase.SUCCEEDED],
            recipients_email=["myboss@example.com"],
        ),
        Slack(
            phases=[
                WorkflowExecutionPhase.SUCCEEDED,
                WorkflowExecutionPhase.ABORTED,
                WorkflowExecutionPhase.TIMED_OUT,
            ],
            recipients_email=["myteam@slack.com"],
        ),
    ],
)


# 4. You can use pyflyte register to register the launch plan and lauch it in flyteconsole to get the notifications.
#
# pyflyte register lp_notifications.py
