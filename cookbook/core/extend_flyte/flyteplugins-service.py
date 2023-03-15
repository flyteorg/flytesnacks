"""
.. _flyteplugins-service:

##################################
Writing a Backend Plugin in Python
##################################

.. tags:: Extensibility, Contribute, Intermediate

Currently, flyteplugins is live in the flytepropeller, which means we have to rebuild flytepropeller if we register a new plugin.
It is hard to implement backend plugins, especially for data-scientists & MLE’s who do not have working knowledge
 of Golang. Also, performance requirements, maintenance and development is cumbersome

We build a new component in flyte calle ``flyteplugins-service``, some goal behind this,
- Plugins should be easy to author - no need of code generation, using tools that MLEs and Data Scientists are not accustomed to using.
- Most important plugins for Flyte today are plugins that communicate with external services.
- It should be possible to test these plugins independently and also deploy them privately.
- It should be possible for users to use backend plugins for local development, especially in flytekit and unionML
- It should be possible to author plugins in any language.
- Plugins should be scalable
- Plugins should have a very simple API
- Plugins should show up in the UI (extra details)

Register a new plugin
=====================

Flytekit Interface Specification
-------------------------------
To implement a new plugin, users need to extend ``BackendPluginBase``, and it consist 3 methods (create / get / delete).

- Create - Submit a job to external system (like Bigquery, Databricks), and return job id.
- Get - Get current job status.
- Delete - Delete the job.

.. code-block:: python

    class BackendPluginBase:
    def __init__(self, task_type: str):
        self._task_type = task_type

    @property
    def task_type(self) -> str:
        return self._task_type

    @abstractmethod
    def create(
        self, inputs: typing.Optional[LiteralMap], output_prefix: str, task_template: TaskTemplate
    ) -> plugin_system_pb2.TaskCreateResponse:
        pass

    @abstractmethod
    def get(self, job_id: str) -> plugin_system_pb2.TaskGetResponse:
        pass

    @abstractmethod
    def delete(self, job_id: str) -> plugin_system_pb2.TaskDeleteResponse:
        pass

    # To register the custom plugin
    BackendPluginRegistry.register(CustomPlugin())

Build a New image
-----------------
Here is a sample dockerfile for building flyteplugins-service image.

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
          - flyteplugins-service
        default-for-task-types:
          - bigquery_query_job_task: flyteplugins-service
          - custom_plugin: flyteplugins-service

    flyteplugins-service:
      # By default, all the request will be sent to the endpoint.
      defaultGrpcEndpoint: flyte-sandbox.flyte.svc.cluster.local:80
      endpointForTaskTypes:
        # It will override the default grpc endpoint for bigquery endpoint, which means propeller will send create request to this endpoint.
        - bigquery_query_job_task: flyte-2.flyte.svc.cluster.local:80

3. Restart the FlytePropeller
"""
