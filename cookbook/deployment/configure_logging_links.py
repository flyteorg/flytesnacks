"""
.. _configure-logging:

Configuring Logging Links in UI
---------------------------------

Often times to debug your workflows in production, you want to access the logs from your tasks as they run. This is different from core Flyte platform logs. These logs are specific to an execution and maybe different for different plugins.
What makes this even harder to create a one size fits all, is that every organization potentially uses different Log aggregators.
This could be Cloud hosted solutions like AWS cloudwatch, GCP Stackdriver, Splunk, Datadog etc.

Flyte, does not have an opinion here and provides a simplified interface to configure your log provider. Flytesandbox ships with using
the Kubernetes dashboard to visualize the logs. This can be not safe for production use and you should potentially use one
of the hosted providers.

How Do I configure?
^^^^^^^^^^^^^^^^^^^^

`Logging structure configuration <https://github.com/flyteorg/flyteplugins/blob/d76eb152eb36b9a77887985ab0ff3be923261bfb/go/tasks/logs/config.go#L37-L41>`_

"""
