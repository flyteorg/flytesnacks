(aws_sagemaker_inference_agent)=

# AWS SageMaker Inference Agent

```{eval-rst}
.. tags:: AWS, Integration, Advanced
```

The AWS SageMaker inference agent allows you to deploy models and create, as well as trigger inference endpoints.
You can also fully remove the SageMaker deployment.

## Installation

To use the AWS SageMaker inference agent, run the following command:

```
pip install flytekitplugins-awssagemaker
```

## Example usage

For a usage example, see {doc}`AWS SageMaker inference agent example usage <sagemaker_inference_agent_example_usage>`.

## Local testing

To test an agent locally, create a class for the agent task that inherits from
[SyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L222-L256)
or [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L259-L354).
These mixins can handle synchronous and synchronous tasks, respectively,
and allow flytekit to mimic FlytePropeller's behavior in calling the agent.
For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

:::{note}
In some cases, you will need to store credentials in your local environment when testing locally.
It should follow the same pattern as
[storing secrets locally](https://docs.flyte.org/en/latest/user_guide/productionizing/secrets.html#secret-discovery).
:::

## Flyte deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the AWS SageMaker inference agent in your Flyte deployment, refer to the
{ref}`AWS SageMaker inference agent setup guide <deployment-agent-setup-sagemaker-inference>`.

```{toctree}
:maxdepth: -1
:hidden:

sagemaker_inference_agent_example_usage
```
