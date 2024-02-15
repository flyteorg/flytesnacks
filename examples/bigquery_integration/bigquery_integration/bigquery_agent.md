(bigquery_agent)=

# BigQuery agent

## Installation

To install the BigQuery agent, run the following command:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-bigquery
```

This agent is purely a spec. Since SQL is completely portable, there is no need to build a Docker container.

## Usage

For an example query, see {doc}`BigQuery example query<bigquery>`.

## Local testing

TK

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To configure your deployment for the BigQuery agent, see the {ref}`BigQuery agent deployment documentation<deployment-agent-setup-bigquery>`.
