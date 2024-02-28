```{eval-rst}
.. tags:: AWS, GCP, AliCloud, Integration, Advanced
```

(mmcloud_agent)=

# Memory Machine Cloud agent

[MemVerge](https://memverge.com/) [Memory Machine Cloud](https://www.mmcloud.io/) (MMCloud)—available on AWS, GCP, and AliCloud—empowers users to continuously optimize cloud resources during runtime, safely execute stateful tasks on spot instances, and monitor resource usage in real time. These capabilities make it an excellent fit for long-running batch workloads. Flyte can be integrated with MMCloud, allowing you to execute Flyte tasks using MMCloud.

## Installation

To install the agent, run the following command:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-mmcloud
```

To get started with Memory Machine Cloud, see the [Memory Machine Cloud user guide](https://docs.memverge.com/mmce/current/userguide/olh/index.html).

## Example usage

For a usage example, see {doc}`Memory Machine Cloud agent example usage<mmcloud_agent_example_usage>`.

## Local testing

To test an agent locally, create a class for the agent task that inherits from [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L155). This mixin can handle both asynchronous tasks and synchronous tasks and allows flytekit to mimic FlytePropeller's behavior in calling the agent. For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

```{note}

In some cases, you will need to store credentials in your local environment when testing locally.

```

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the Memory Machine Cloud agent in your Flyte deployment, see the {ref}`MMCloud agent setup guide <deployment-agent-setup-mmcloud>`.


```{toctree}
:maxdepth: -1
:hidden:

mmcloud_agent_example_usage
```
