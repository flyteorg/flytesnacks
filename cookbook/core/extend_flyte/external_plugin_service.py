"""
.. _extend-external-plugin-system:

##################################
Writing Backend Plugins in Python
##################################

.. tags:: Extensibility, Contribute, Intermediate

Currently, flyteplugins is live in the flytepropeller, which means we have to rebuild flytepropeller if we register a new plugin.
 It is hard to implement backend plugins, especially for data scientists & MLEs who do not have working knowledge of Golang.
  Also, performance requirements, maintenance, and development are cumbersome.


Key goals of the external plugin system include:
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
The External Plugin System serves as a Python-based plugin registry powered by a gRPC server. It allows users and Propeller to send gRPC requests to the registry for executing jobs such as BigQuery and Databricks. Notably, the registry is designed to be stateless, ensuring effortless scalability of the system as needed.

.. figure:: https://i.ibb.co/y0MhBfn/Screen-Shot-2023-04-16-at-11-51-17-PM.png
  :alt: External-Plugin-System
  :class: with-shadow

How to register a new plugin
=====================

Flytekit interface specification
--------------------------------
To register new backend plugins, you can extend the ``BackendPluginBase`` class in the flytekit backend module. Implementing the following three methods is necessary, and it's important to ensure that all calls are idempotent:

- ``create``: This method is used to initiate a new task. Users have the flexibility to use gRPC, REST, or SDK to create a task.
- ``get``: This method allows retrieving the job ID associated with the task, such as a BigQuery Job ID or Databricks task ID.
- ``delete``: Invoking this method will send a request to delete the corresponding job.

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
The following is a sample Dockerfile for building an image for an external plugin system.

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
          - custom_task: external-plugin-service

    flyteplugins-service:
      # By default, all the request will be sent to the default endpoint.
      defaultGrpcEndpoint: "dns:///external-plugin-service-production.flyte.svc.cluster.local:80"
      supportedTaskTypes:
        - custom_task
      endpointForTaskTypes:
        # It will override the default grpc endpoint for bigquery endpoint, which means propeller will send create request to this endpoint.
        - bigquery_query_job_task: "dns:///external-plugin-service-development.flyte.svc.cluster.local:80"

3. Restart the FlytePropeller
"""
