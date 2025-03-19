(slurm_agent)=

# Slurm agent

```{eval-rst}
.. tags:: Integration, HighPerformanceComputing, Advanced
```

## Installation

To install the Slurm agent, run the following command:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-slurm
```

## Example usage

For the example usage of different Slurm task types, please see {doc}`Slurm agent example usage<slurm_agent_example_usage>`.

## Local testing

To test the Slurm agent locally, create a class for the agent task that inherits from [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/cd6bd01ad0ba6688afc71a33a59ece53f90e841a/flytekit/extend/backend/base_agent.py#L3). This mixin can handle asynchronous tasks and allows flytekit to mimic FlytePropeller's behavior in calling the agent. For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_in_a_local_python_environment.html)".

```{note}
In some cases, you will need to store credentials in your local environment when testing locally.
```

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the Slurm agent in your Flyte deployment, see the {ref}`Slurm agent deployment guide<deployment-agent-setup-slurm>`.


```{toctree}
:maxdepth: -1
:hidden:

slurm_agent_example_usage
```