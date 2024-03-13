(airflow_agent)=

# Airflow agent

[Apache Airflow](https://airflow.apache.org) is a widely used open source platform for managing workflows with a robust ecosystem. Flyte provides an Airflow plugin that allows you to run Airflow tasks as Flyte tasks.
This allows you to use the Airflow plugin ecosystem in conjunction with Flyte's powerful task execution and orchestration capabilities.

```{note}
The Airflow agent does not support all [Airflow operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html). We have tested many, but if you run into issues, please [file a bug report](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=bug%2Cuntriaged&projects=&template=bug_report.yaml&title=%5BBUG%5D+).
```

## Installation

To install the plugin, run the following command:

`pip install flytekitplugins-airflow`

This plugin has two components:
* **Airflow compiler:** This component compiles Airflow tasks to Flyte tasks, so Airflow tasks can be directly used inside the Flyte workflow.
* **Airflow agent:** This component allows you to execute Airflow tasks either locally or on a Flyte cluster.

## Example usage

```{note}

You don't need an Airflow cluster to run Airflow tasks, since flytekit will
automatically compile Airflow tasks to Flyte tasks and execute them on the Airflow agent.

```

For a usage example, see {doc}`Airflow agent example usage<airflow_agent_example_usage>`.

## Local testing

Airflow doesn't support local execution natively. However, Flyte compiles Airflow tasks to Flyte tasks,
which enables you to test Airflow tasks locally in flytekit's local execution mode.


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
airflow_agent_example_usage
```
