(bigquery_agent)=

# BigQuery agent

## Installation

To install the BigQuery agent, run the following command:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-bigquery
```

This agent is purely a spec. Since SQL is completely portable, there is no need to build a Docker container.

## Example usage

For an example query, see {doc}`BigQuery agent example usage<bigquery_agent_example_usage>`.

## Local testing

To test an agent locally, create a class for the agent task that inherits from [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L155). This mixin can handle both asynchronous tasks and synchronous tasks and allows flytekit to mimic FlytePropeller's behavior in calling the agent. For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

```{note}

In some cases, you will need to store credentials in your local environment when testing locally.

```

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the BigQuery agent in your Flyte deployment, see the {ref}`BigQuery agent deployment guide<deployment-agent-setup-bigquery>`.


```{toctree}
:maxdepth: -1
:hidden:

bigquery_agent_example_usage

```
