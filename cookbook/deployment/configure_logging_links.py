"""
.. _configure-logging:

Configuring Logging Links in UI
---------------------------------

Often times to debug your workflows in production, you want to access the logs from your tasks as they run.
This is different from core Flyte platform logs. These logs are specific to an execution and maybe different for
the various plugins (For example spark may have driver and executor logs).
Every organization potentially uses different log aggregators, which makes it hard to create a one size fits all solution.
Some examples of the Log aggregators are Cloud hosted solutions like AWS cloudwatch, GCP Stackdriver, Splunk, Datadog etc.

Flyte, does not have an opinion here and provides a simplified interface to configure your log provider. Flyte-sandbox
ships with the Kubernetes dashboard to visualize the logs. This may not be safe for production and we recommend users
explore other Log Aggregators.

How Do I configure?
^^^^^^^^^^^^^^^^^^^^

`Logging structure configuration <https://github.com/flyteorg/flyteplugins/blob/d76eb152eb36b9a77887985ab0ff3be923261bfb/go/tasks/logs/config.go#L37-L41>`_

"""
