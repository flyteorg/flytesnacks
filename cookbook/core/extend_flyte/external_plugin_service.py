"""
.. _external-plugin-system

##################################
Writing a Backend Plugin in Python
##################################

.. tags:: Extensibility, Contribute, Intermediate

Currently, flyteplugins is live in the flytepropeller, which means we have to rebuild flytepropeller if we register a new plugin.
It is hard to implement backend plugins, especially for data-scientists & MLE’s who do not have working knowledge
 of Golang. Also, performance requirements, maintenance and development is cumbersome

We build a new component in flyte called ``external-plugin-system``, some goal behind this,
- Plugins should be easy to author - no need of code generation, using tools that MLEs and Data Scientists are not accustomed to using.
- Most important plugins for Flyte today are plugins that communicate with external services.
- It should be possible to test these plugins independently and also deploy them privately.
- It should be possible for users to use backend plugins for local development, especially in flytekit and unionML
- It should be possible to author plugins in any language.
- Plugins should be scalable
- Plugins should have a very simple API
- Plugins should show up in the UI (extra details)

Overview
========
The External Plugin System is a Python-based plugin registry that uses a gRPC server. Users and Propeller can send gRPC
 requests to this registry to run jobs, such as BigQuery and Databricks. Furthermore, the registry is stateless,
  which makes it easy to scale the system up or down.

.. figure:: https://file.notion.so/f/s/f1cdc46e-88f9-4b11-bec5-19629074d5a9/Untitled.png?id=0b3e45f9-7d32-47a0-8a74-a4ecf1ca00e8&table=block&spaceId=644c92b6-6f64-49fa-96f0-e0a1ece8cb94&expirationTimestamp=1680617867407&signature=1y-rlyarnDWJ0twBolvUFMMA8vTqIkD-HkEMfNtHhpM&downloadName=Untitled.png
  :alt: MLflow UI
  :class: with-shadow

Register a new plugin
=====================

Flytekit Interface Specification
-------------------------------
To register a new backend plugin, user have to extend `BackendPluginBase` in the flytekit backend module.
 Users have to implement below 3 methods, and all the call should be idempotent.

- `create` is used to launch a new task. People can use gRPC, REST, or SDK to create a task.
- `get` is used to get the jobID (like BigQuery Job ID or Databricks task ID).
- `delete` Will send a request to delete the job.

.. code-block:: python

    class BackendPluginBase:
    def __init__(self, task_type: str):
        self._task_type = task_type

    @property
    def task_type(self) -> str:
        return self._task_type

    @abstractmethod
    def create(
        self,
        context: grpc.ServicerContext,
        output_prefix: str,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
    ) -> TaskCreateResponse:
        pass

    @abstractmethod
    def get(self, context: grpc.ServicerContext, job_id: str) -> TaskGetResponse:
        pass

    @abstractmethod
    def delete(self, context: grpc.ServicerContext, job_id: str) -> TaskDeleteResponse:
        pass

    # To register the custom plugin
    BackendPluginRegistry.register(CustomPlugin())

Build a New image
-----------------
Here is a sample dockerfile for building a image for external plugin system.

.. code-block:: Dockerfile

    FROM python:3.9-slim-buster

    MAINTAINER Flyte Team <users@flyte.org>
    LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

    WORKDIR /root
    ENV PYTHONPATH /root

    # flytekit will auto load the plugin if package is installed.
    RUN pip install flytekitplugins-bigquery
    CMD pyflyte serve --port 80

Update Helm Chart
-----------------
1. Update the `images <https://github.com/flyteorg/flyte/pull/3454/files#diff-cbcadfa3abd9e4771deaab1b0f28d2c7f6a67f3ebd9b1b1ec6a0eebb38a718e4R142-R146>`__
2. Update the FlytePropeller configmap.

.. code-block:: YAML

    tasks:
      task-plugins:
        enabled-plugins:
          - external-plugin-service
        default-for-task-types:
          - bigquery_query_job_task: external-plugin-service
          - custom_plugin: external-plugin-service

    flyteplugins-service:
      # By default, all the request will be sent to the default endpoint.
      defaultGrpcEndpoint: flyte-sandbox.flyte.svc.cluster.local:80
      endpointForTaskTypes:
        # It will override the default grpc endpoint for bigquery endpoint, which means propeller will send create request to this endpoint.
        - bigquery_query_job_task: "flyte-2.flyte.svc.cluster.local:80"

3. Restart the FlytePropeller
"""
