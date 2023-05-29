"""
.. _extend-agent-service:

########################
Writing Agents in Python
########################

.. tags:: Extensibility, Contribute, Intermediate

Implementing backend plugins can be challenging, particularly for data scientists and MLEs who lack proficiency in
 Golang. Additionally, managing performance requirements, maintenance, and development can be burdensome.
  To address these issues, we introduced the "Agent Service" in Flyte. This system enables rapid plugin
   development while decoupling them from the core flytepropeller engine.


Key goals of the agent service include:
- Easy plugin authoring: Plugins can be authored without the need for code generation or unfamiliar tools.
- Support for communication with external services: The focus is on enabling plugins that seamlessly interact with external services.
- Independent testing and private deployment: Plugins can be tested independently and deployed privately, providing flexibility and control over plugin development.
- Backend plugin usage in local development: Users, especially in flytekit and unionML, can leverage backend plugins for local development, streamlining the development process.
- Language-agnostic plugin authoring: Plugins can be authored in any programming language, allowing users to work with their preferred language and tools.
- Scalability: Plugins are designed to be scalable, ensuring they can handle large-scale workloads effectively.
- Simple API: Plugins offer a straightforward API, making integration and usage straightforward for developers.
- UI integration: Plugins are visible in the Flyte UI, providing additional details and enhancing the user experience.

Overview
========
The Flyte Agent Service serves as a Python-based plugin registry powered by a gRPC server. It allows users and Propeller
 to send gRPC requests to the registry for executing jobs such as BigQuery and Databricks. Notably, the registry is
  designed to be stateless, ensuring effortless scalability of the system as needed.

.. figure:: https://i.ibb.co/vXhBDjP/Screen-Shot-2023-05-29-at-2-54-14-PM.png
  :alt: Agent Service
  :class: with-shadow

How to register a new plugin
============================

Flytekit interface specification
--------------------------------
To register new backend plugins, you can extend the ``BackendPluginBase`` class in the flytekit backend module. Implementing the following three methods is necessary, and it's important to ensure that all calls are idempotent:

- ``create``: This method is used to initiate a new task. Users have the flexibility to use gRPC, REST, or SDK to create a task.
- ``get``: This method allows retrieving the job ID associated with the task, such as a BigQuery Job ID or Databricks task ID.
- ``delete``: Invoking this method will send a request to delete the corresponding job.

.. code-block:: python

    from flytekit.extend.backend.base_plugin import BackendPluginBase, BackendPluginRegistry

    class CustomPlugin(BackendPluginBase):
        def __init__(self, task_type: str):
            self._task_type = task_type

        def create(
            self,
            context: grpc.ServicerContext,
            output_prefix: str,
            task_template: TaskTemplate,
            inputs: typing.Optional[LiteralMap] = None,
        ) -> TaskCreateResponse:
            pass

        def get(self, context: grpc.ServicerContext, job_id: str) -> TaskGetResponse:
            pass

        def delete(self, context: grpc.ServicerContext, job_id: str) -> TaskDeleteResponse:
            pass

    # To register the custom plugin
    BackendPluginRegistry.register(CustomPlugin())

Here is an example of `BigQuery backend plugin <https://github.com/flyteorg/flytekit/blob/eafcc820303367749e63edc62190b9153fd6be5e/plugins/flytekit-bigquery/flytekitplugins/bigquery/backend_plugin.py#LL94C32-L94C48>`__ implementation.

Build a New image
-----------------
The following is a sample Dockerfile for building an image for a flyte agent service.

.. code-block:: Dockerfile

    FROM python:3.9-slim-buster

    MAINTAINER Flyte Team <users@flyte.org>
    LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

    WORKDIR /root
    ENV PYTHONPATH /root

    # flytekit will autoload the plugin if package is installed.
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
          - agent-service
        default-for-task-types:
          - bigquery_query_job_task: agent-service
          - custom_task: agent-service

    agent-service:
      # By default, all the request will be sent to the default endpoint.
      defaultGrpcEndpoint: "dns:///agent-service-production.flyte.svc.cluster.local:80"
      supportedTaskTypes:
        - custom_task
      endpointForTaskTypes:
        # It will override the default grpc endpoint for bigquery endpoint, which means propeller will send create request to this endpoint.
        - bigquery_query_job_task: "dns:///agent-service-development.flyte.svc.cluster.local:80"

3. Restart the FlytePropeller

.. code-block::

    kubectl rollout restart deployment flytepropeller -n flyte

"""
