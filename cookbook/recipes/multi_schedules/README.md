# How do I create schedules?

If you haven't read yet the [Launch Plans](https://docs.lyft.net/eng/flytedocs/user/concepts/launchplans_schedules.html#launch-plans) part of the documentation, please do so as it explains the basics of launch plans and schedules.

Schedules are set on launch plans, and as you can see from the [IDL](https://github.com/lyft/flyteidl/blob/e9727afcedf8d4c30a1fc2eeac45593e426d9bb0/protos/flyteidl/admin/schedule.proto#L20) can be either set with a traditional cron expression, or an interval.

Note that, for convenience, when Flyte Admin launches a scheduled execution, it will include the scheduled time as an input argument, if you wish.  To use this feature, simply supply the name of the input that you'd like to receive it under to the schedule.  To clarify this is the scheduled time, not the time it actually launches - there's always going to be a few seconds worth of delay.

Flyte uses common cron expression syntax so something like this will run every fifteen minutes, every day, from the top of the hour.

```python
SCHEDULE_EXPR = "0/15 * * * ? *"
```

The `create_launch_plan` function can take a schedule expression

```python
from recipes.compose.inner import IdentityWorkflow
from flytekit.common import schedules
with_cron_schedule = IdentityWorkflow.create_launch_plan(
    schedule=schedules.CronSchedule(SCHEDULE_EXPR),
)
```

A similar result can be achieved with a fixed rate i

```python
import datetime
with_fixed_schedule = IdentityWorkflow.create_launch_plan(
    schedule=schedules.FixedRate(datetime.timedelta(minutes=15),
)
```
If your workflow takes a datetime as an input named `scheduled_datetime` and you would like it to receive the scheduled time at launch, you can specify it as,
```python
scheduled_time_lp = MyWorkflow.create_launch_plan(
    schedule=schedules.CronSchedule(SCHEDULE_EXPR, kickoff_time_input_arg='scheduled_datetime'),
)
```