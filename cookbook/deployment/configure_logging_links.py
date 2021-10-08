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

To configure your log provider, the provider needs to support `URL` links that are sharable and can be templatized.
The templating engine has access to `there <https://github.com/flyteorg/flyteplugins/blob/b0684d97a1cf240f1a44f310f4a79cc21844caa9/go/tasks/pluginmachinery/tasklog/plugin.go#L7-L16>`_ parameters.

The parameters can be used to generate a unique URL to the logs that pertain to this specific task using a templated URI. The templated URI has access to the following parameters,

- {{ .podName }}: Gets the pod name as it shows in k8s dashboard,
- {{ .namespace }}: K8s namespace where the pod runs,
- {{ .containerName }}: The container name that generated the log,
- {{ .containerId }}: The container id docker/crio generated at run time,
- {{ .logName }}: A deployment specific name where to expect the logs to be.
- {{ .hostname }}: The hostname where the pod is running and where logs reside.
- {{ .podUnixStartTime }}: The pod creation time (in unix seconds, not millis)
- {{ .podUnixFinishTime }}: Don't have a good mechanism for this yet, but approximating with time.Now for now

The parameterization engine uses Golangs native templating format and hence ``{{ }}``. An example configuration can be as follows

.. code-block:: yaml

task_logs:
  plugins:
    logs:
      displayName: <name-to-show>
      templateUris:
        - "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logEventViewer:group=/flyte-production/kubernetes;stream=var.log.containers.{{.podName}}_{{.namespace}}_{{.containerName}}-{{.containerId}}.log"
        - "https://some-other-source/home?region=us-east-1#logEventViewer:group=/flyte-production/kubernetes;stream=var.log.containers.{{.podName}}_{{.namespace}}_{{.containerName}}-{{.containerId}}.log"
      messageFormat: "unknown" | "csv" | "json"

This will output two logs per task that uses the log plugin. Not all task types use the log plugin, for example the Sagemaker plugin, will use the logs output provided by Sagemaker, Snowflake plugin, will use a link to the snowflake console.
"""
