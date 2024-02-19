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

TK

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
