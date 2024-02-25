(airflow_agent)=

# Airflow agent

```{note}
The Airflow agent does not support all [Airflow operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html). We have tested many, but if you run into issues, please [file a bug report](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=bug%2Cuntriaged&projects=&template=bug_report.yaml&title=%5BBUG%5D+).
```

## Installation

To install the plugin, run the following command:

`pip install flytekitplugins-airflow`

## Example usage

```{note}

You don't need an Airflow cluster to run Airflow tasks, since Flytekit will
automatically compile Airflow tasks to Flyte tasks and execute them on the Flyte cluster.

```

For a usage example, see the {doc}`Airflow agent example <airflow_agent_example>` page.

## Local testing

To test an agent locally, create a class for the agent task that inherits from [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L155). This mixin can handle both asynchronous tasks and synchronous tasks and allows flytekit to mimic FlytePropeller's behavior in calling the agent. For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

```{note}

In some cases, you will need to store credentials in your local environment when testing locally.

```

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the Airflow agent in your Flyte deployment, see the {ref}`Airflow agent deployment guide<deployment-agent-setup-airflow>`.

```{toctree}
:maxdepth: -1
:hidden:
airflow_agent_example
```