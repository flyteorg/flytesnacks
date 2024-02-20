(snowflake_agent)=

# Snowflake agent

## Installation

To use the Snowflake plugin, run the following command:

```
pip install flytekitplugins-snowflake
```

## Example usage

For a usage example, see the {ref}`Snowflake example page <snowflake>`.

## Local testing

To test an agent locally, create a class for the agent task that inherits from [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L155). This mixin can handle both asynchronous tasks and synchronous tasks and allows flytekit to mimic FlytePropeller's behavior in calling the agent. For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

```{note}

In some cases, you will need to store credentials in your local environment when testing locally.

```

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the Snowflake agent in your Flyte deployment, see the {ref}`Snowflake agent setup guide <deployment-agent-setup-snowflake>`.
