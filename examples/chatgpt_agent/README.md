(chatgpt_agent)=

# ChatGPT agent

## Installation

To install the ChatGPT agent, run the following command:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-chatgpt
```

## Example usage

For an example job, see {doc}`ChatGPT agent example usage<chatgpt_agent_example_usage>`.

## Local testing

To test an agent locally, create a class for the agent task that inherits from [SyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L225). This mixin can handle synchronous tasks and allows flytekit to mimic FlytePropeller's behavior in calling the agent. For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

```{note}

In some cases, you will need to store credentials in your local environment when testing locally.

```

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the ChatGPT agent in your Flyte deployment, see the {ref}`ChatGPT agent deployment guide<deployment-agent-setup-chatgpt>`.


```{toctree}
:maxdepth: -1
:hidden:

chatgpt_agent_example_usage

```
