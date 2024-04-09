# Scheduling workflows

from datetime import datetime

from flytekit import task, workflow


@task
def format_date(run_date: datetime) -> str:
    return run_date.strftime("%Y-%m-%d %H:%M")


@workflow
def date_formatter_wf(kickoff_time: datetime):
    formatted_kickoff_time = format_date(run_date=kickoff_time)
    print(formatted_kickoff_time)


from flytekit import CronSchedule, LaunchPlan  # noqa: E402

# creates a launch plan that runs every minute.
cron_lp = LaunchPlan.get_or_create(
    name="my_cron_scheduled_lp",
    workflow=date_formatter_wf,
    schedule=CronSchedule(
        # Note that the ``kickoff_time_input_arg`` matches the workflow input we defined above: kickoff_time
        # But in case you are using the AWS scheme of schedules and not using the native scheduler then switch over the schedule parameter with cron_expression
        schedule="*/1 * * * *",  # Following schedule runs every min
        kickoff_time_input_arg="kickoff_time",
    ),
)

# If you prefer to use an interval rather than a cron scheduler to schedule
# your workflows, you can use the fixed-rate scheduler.
# A fixed-rate scheduler runs at the specified interval.
from datetime import timedelta  # noqa: E402

from flytekit import FixedRate, LaunchPlan  # noqa: E402


@task
def be_positive(name: str) -> str:
    return f"You're awesome, {name}"


@workflow
def positive_wf(name: str):
    reminder = be_positive(name=name)
    print(f"{reminder}")


fixed_rate_lp = LaunchPlan.get_or_create(
    name="my_fixed_rate_lp",
    workflow=positive_wf,
    # Note that the workflow above doesn't accept any kickoff time arguments.
    # We just omit the ``kickoff_time_input_arg`` from the FixedRate schedule invocation
    schedule=FixedRate(duration=timedelta(minutes=10)),
    fixed_inputs={"name": "you"},
)
