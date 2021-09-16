.. _scheduled_workflows:

Scheduling Workflows
--------------------

For background on launch plans, refer to :any:`launch_plans`.

Launch plans can be set to run automatically on a schedule using the flyte native scheduler which is enabled by default in sandbox environment
For workflows that depend on knowing the kick-off time, Flyte also supports passing in the scheduled time (not the actual time, which may be a few seconds off) as an argument to the workflow.
