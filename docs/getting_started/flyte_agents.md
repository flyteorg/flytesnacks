---
# override the toc-determined page navigation order
prev-page: getting_started/extending_flyte
prev-page-title: Extending Flyte
---

(getting_started_flyte_agents)=
# About Flyte agents

In Flyte, an agent is a long-running stateless service powered by a gRPC server that executes a specific type of task -- for example, the BigQuery agent runs BigQuery tasks. Each agent service is a Kubernetes deployment that receives gRPC requests from FlytePropeller and executes jobs. You can create different agent services that host different agents -- for example, a production and a development agent service.

:::{figure} https://i.ibb.co/vXhBDjP/Screen-Shot-2023-05-29-at-2-54-14-PM.png
:alt: Agent Service
:class: with-shadow
:::

## End users

TK - benefits of agents for end users:

* Agents interact seamlessly with external services.
* Agents reduce the overhead of creating a pod for each task.
* Agents are designed to be scalable, ensuring they can handle large workloads efficiently.
* End users can use agents for local development without having to change backend configuration, streamlining the development process.
* Agents decrease load on FlytePropeller, since the agent service runs outside of FlytePropeller.

To use agents in your tasks, see {doc}`"Using Flyte agents in tasks"<using_flyte_agents_in_tasks>`

## Contributors

TK - benefits of agents for contributors:

The Flyte agent framework enables rapid agent development since agents are decoupled from the core FlytePropeller engine. If you create a new type of task, we recommend creating a new agent to run it rather than running the task in the pod. You can update the FlytePropeller configMap to specify which agent that should execute which type of task.

* Agents can be written in any programming language, allowing you to work with your preferred language and tools. (For now, we only support Python agents, but we may support other languages in the future.)
* Agents offer a straightforward API, making integration and usage easy for developers.
* Agents can be tested independently and deployed privately, making maintenance easier and providing flexibility and control over development.

To create Flyte agents, see {doc}`"Creating Flyte agents"<creating_flyte_agents>`


```{toctree}
:maxdepth: -1
:hidden:

using_flyte_agents_in_tasks
creating_flyte_agents
testing_flyte_agents_locally
configuring_your_flyte_deployment_for_agents
```
