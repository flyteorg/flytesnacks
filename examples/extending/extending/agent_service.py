# %% [markdown]
# (extend-agent-service)=
#
# # Writing Flyte Agents in Python
#
# ```{eval-rst}
# .. tags:: Extensibility, Contribute, Intermediate
# ```
#
# :::{note}
# This is an experimental feature, which is subject to change in the future.
# :::
#
# ## About the Flyte Agent service
#
# The Flyte Agent service is a Python-based service powered by a gRPC server. It allows FlytePropeller
# to send gRPC requests to the agent service for executing jobs—for instance, BigQuery and Databricks jobs. Each Flye Agent service is a Kubernetes
# deployment. You can create different Flyte Agent services to host different Flyte Agents. For example, you could have one production
# agent service and one development agent service.
#
# Key goals of the agent service:
# * Support for communication with external services: The focus is on enabling agents that seamlessly interact with external services.
# * Independent testing and private deployment: Agents can be tested independently and deployed privately, providing flexibility and control over development.
# * Flyte Agent usage in local development: Users, especially in flytekit, can leverage backend agents for local development, streamlining the development process.
# * Language-agnostic: Agents can be authored in any programming language, allowing users to work with their preferred language and tools.
# * Scalability: Agents are designed to be horizontally scalable. Agents are stateless services, ensuring they can handle large-scale workloads effectively.
# * Simple API: Agents offer a straightforward API, making integration and usage straightforward for developers.
#
# :::{figure} https://i.ibb.co/vXhBDjP/Screen-Shot-2023-05-29-at-2-54-14-PM.png
# :alt: Agent Service
# :class: with-shadow
# :::
#
# ## About Flyte Agents
# A Flyte Agent is intended to run a specific type of task. For example, a BigQuery Flyte Agent runs BigQuery tasks.
#
# Flyte Agents are preferable to FlytePropeller plugins for interacting with external services. With a FlytePropeller plugin,
# you need to implement a plugin that is responsible for creating a CRD or submitting an HTTP request to the external service,
# which increases the complexity of FlytePropeller. Such a plugin is hard to maintain, as FlytePropeller needs to be updated and compiled, and hard to test.
# Additionally, since the FlytePropeller plugin runs in FlytePropeller itself, it increases the load on the FlytePropeller engine.
#
# ## Creating a new Flyte Agent
#
# To create a new Flyte Agent, extend the `AgentBase` class in the flytekit backend module and implement the following three methods. All calls must be idempotent:
#
# - `create`: Initiates a new task. Users have the flexibility to use gRPC, REST, or an SDK to create a task.
# - `get`: Retrieves the job Resource (jobID or output literal) associated with the task, such as a BigQuery Job ID or Databricks task ID.
# - `delete`: Sends a request to delete the corresponding job.
#
# ```python
# from flytekit.extend.backend.base_agent import AgentBase, AgentRegistry
# from dataclasses import dataclass
# import requests
#
# @dataclass
# class Metadata:
#     # you can add any metadata you want, propeller will pass the metadata to the agent to get the job status.
#     # For example, you can add the job_id to the metadata, and the agent will use the job_id to get the job status.
#     # You could also add the s3 file path, and the agent can check if the file exists.
#     job_id: str
#
# class CustomAgent(AgentBase):
#     def __init__(self, task_type: str):
#         # Each agent should have a unique task type. Agent service will use the task type to find the corresponding agent.
#         self._task_type = task_type
#
#     def create(
#         self,
#         context: grpc.ServicerContext,
#         output_prefix: str,
#         task_template: TaskTemplate,
#         inputs: typing.Optional[LiteralMap] = None,
#     ) -> TaskCreateResponse:
#         # 1. Submit the task to the external service (BigQuery, DataBricks, etc.)
#         # 2. Create a task metadata such as jobID.
#         # 3. Return the task metadata, and keep in mind that the metadata should be serialized to bytes.
#         res = requests.post(url, json=data)
#         return CreateTaskResponse(resource_meta=json.dumps(asdict(Metadata(job_id=str(res.job_id)))).encode("utf-8"))
#
#     def get(self, context: grpc.ServicerContext, resource_meta: bytes) -> TaskGetResponse:
#         # 1. Deserialize the metadata.
#         # 2. Use the metadata to get the job status.
#         # 3. Return the job status.
#         metadata = Metadata(**json.loads(resource_meta.decode("utf-8")))
#         res = requests.get(url, json={"job_id": metadata.job_id})
#         return GetTaskResponse(resource=Resource(state=res.state)
#
#     def delete(self, context: grpc.ServicerContext, resource_meta: bytes) -> TaskDeleteResponse:
#         # 1. Deserialize the metadata.
#         # 2. Use the metadata to delete the job.
#         # 3. If failed to delete the job, add the error message to the grpc context.
#         #   context.set_code(grpc.StatusCode.INTERNAL)
#         #   context.set_details(f"failed to create task with error {e}")
#         try:
#             metadata = Metadata(**json.loads(resource_meta.decode("utf-8")))
#             requests.delete(url, json={"job_id": metadata.job_id})
#         except Exception as e:
#             logger.error(f"failed to delete task with error {e}")
#             context.set_code(grpc.StatusCode.INTERNAL)
#             context.set_details(f"failed to delete task with error {e}")
#         return DeleteTaskResponse()
#
# # To register the custom agent
# AgentRegistry.register(CustomAgent())
# ```
# 
# Here is an example of a [BigQuery Agent](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-bigquery/flytekitplugins/bigquery/agent.py) implementation.
#
# ## Testing a Flyte Agent
#
# Agents can be tested locally without running the Flyte backend server.
#
# The task inherited from AsyncAgentExecutorMixin can be executed locally, allowing flytekit to mimic FlytePropeller's behavior to call the agent.
# In some cases, you should store credentials in your local environment when testing locally.
# For example, you need to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable when testing the BigQuery task.
# After setting up the credentials, you can run the task locally. Flytekit will automatically call the agent to `create`, `get`, or `delete` the task.
#
# ```python
# bigquery_doge_coin = BigQueryTask(
#     name=f"bigquery.doge_coin",
#     inputs=kwtypes(version=int),
#     query_template="SELECT * FROM `bigquery-public-data.crypto_dogecoin.transactions` WHERE version = @version LIMIT 10;",
#     output_structured_dataset_type=StructuredDataset,
#     task_config=BigQueryConfig(ProjectID="flyte-test-340607")
# )
# ```
#
# Task above task as an example. You can run the task locally and test the Agent with the following command:
#
# ```bash
# pyflyte run wf.py bigquery_doge_coin --version 10
# ```
#
# ## Building a new image for a Flyte Agent
#
# The following is a sample Dockerfile for building an image for a Flyte Agent.
#
# ```Dockerfile
# FROM python:3.9-slim-buster
#
# MAINTAINER Flyte Team <users@flyte.org>
# LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit
#
# WORKDIR /root
# ENV PYTHONPATH /root
#
# # flytekit will autoload the agent if package is installed.
# RUN pip install flytekitplugins-bigquery
# CMD pyflyte serve agent --port 8000
# ```
#
# :::{note}
# For flytekit versions `<=v1.10.2`, use `pyflyte serve`.
# For flytekit versions `>v1.10.2`, use `pyflyte serve agent`.
# :::
#
# ## Updating Flyte Agents
#
# 1. Update the Flyte Agent deployment's [image](https://github.com/flyteorg/flyte/blob/master/charts/flyteagent/templates/agent/deployment.yaml#L26)
# 2. Update the FlytePropeller configmap.
#
# ```YAML
# tasks:
#   task-plugins:
#     enabled-plugins:
#       - agent-service
#     default-for-task-types:
#       - bigquery_query_job_task: agent-service
#       - custom_task: agent-service
#
# plugins:
#   agent-service:
#     supportedTaskTypes:
#       - bigquery_query_job_task
#       - default_task
#       - custom_task
#     # By default, all the request will be sent to the default agent.
#     defaultAgent:
#       endpoint: "dns:///flyteagent.flyte.svc.cluster.local:8000"
#       insecure: true
#       timeouts:
#         GetTask: 200ms
#       defaultTimeout: 50ms
#     agents:
#       custom_agent:
#         endpoint: "dns:///custom-flyteagent.flyte.svc.cluster.local:8000"
#         insecure: false
#         defaultServiceConfig: '{"loadBalancingConfig": [{"round_robin":{}}]}'
#         timeouts:
#           GetTask: 100ms
#         defaultTimeout: 20ms
#     agentForTaskTypes:
#       # It will override the default agent for custom_task, which means propeller will send the request to this agent.
#       - custom_task: custom_agent
# ```
#
# 3. Restart the FlytePropeller
#
# ```
# kubectl rollout restart deployment flytepropeller -n flyte
# ```
#
