(airflow_agent)=

# Airflow agent

```{note}
Not all Airflow operators are supported. We have tested many, but please help us test them all and [file a bug report](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=bug%2Cuntriaged&projects=&template=bug_report.yaml&title=%5BBUG%5D+) if you have any issues.
```

## Installation

To install the plugin, run the following command:

`pip install flytekitplugins-airflow`

## Example usage

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
