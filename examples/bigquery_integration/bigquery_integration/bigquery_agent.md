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

For an example query, see {doc}`BigQuery example query<bigquery>`.

## Local testing

TK

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the BigQuery agent in your Flyte deployment, see the {ref}`BigQuery agent deployment guide<deployment-agent-setup-bigquery>`.
