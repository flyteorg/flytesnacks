# %% [markdown]
# # Customizing Task Resources
#
# ```{eval-rst}
# .. tags:: Deployment, Infrastructure, Basic
# ```
#
# One of the reasons to use a hosted Flyte environment is the potential of leveraging CPU, memory and storage resources, far greater than what's available locally.
# Flytekit makes it possible to specify these requirements declaratively and close to where the task itself is declared.

# %% [markdown]
# In this example, the memory required by the function increases as the dataset size increases.
# Large datasets may not be able to run locally, so we would want to provide hints to the Flyte backend to request for more memory.
# This is done by decorating the task with the hints as shown in the following code sample.
#
# Tasks can have `requests` and `limits` which mirror the native [equivalents in Kubernetes](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits).
# A task can possibly be allocated more resources than it requests, but never more than its limit.
# Requests are treated as hints to schedule tasks on nodes with available resources, whereas limits
# are hard constraints.
#
# For either a request or limit, refer to the {py:class}`flytekit:flytekit.Resources` documentation.
#
# The following attributes can be specified for a `Resource`.
#
# 1. `cpu`
# 2. `mem`
# 3. `gpu`
#
# To ensure that regular tasks that don't require GPUs are not scheduled on GPU nodes, a separate node group for GPU nodes can be configured with [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).
#
# To ensure that tasks that require GPUs get the needed tolerations on their pods, set up FlytePropeller using the following [configuration](https://github.com/flyteorg/flytepropeller/blob/v0.10.5/config.yaml#L51,L56). Ensure that this toleration config matches the taint config you have configured to protect your GPU providing nodes from dealing with regular non-GPU workloads (pods).
#
# The actual values follow the [Kubernetes convention](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes).
# Let's look at an example to understand how to customize resources.

# %% [markdown]
# Import the dependencies.
# %%
import typing

from flytekit import Resources, task, workflow


# %% [markdown]
# Define a task and configure the resources to be allocated to it.
# %%
@task(requests=Resources(cpu="1", mem="100Mi"), limits=Resources(cpu="2", mem="150Mi"))
def count_unique_numbers(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# %% [markdown]
# Define a task that computes the square of a number.
# %%
@task
def square(x: int) -> int:
    return x * x


# %% [markdown]
# You can use the tasks decorated with memory and storage hints like regular tasks in a workflow.
# %%
@workflow
def my_workflow(x: typing.List[int]) -> int:
    return square(x=count_unique_numbers(x=x))


# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(count_unique_numbers(x=[1, 1, 2]))
    print(my_workflow(x=[1, 1, 2]))

# %% [markdown]
# :::{note}
# To alter the limits of the default platform configuration, change the [admin config](https://github.com/flyteorg/flyte/blob/b16ffd76934d690068db1265ac9907a278fba2ee/deployment/eks/flyte_helm_generated.yaml#L203-L213) and [namespace level quota](https://github.com/flyteorg/flyte/blob/b16ffd76934d690068db1265ac9907a278fba2ee/deployment/eks/flyte_helm_generated.yaml#L214-L240) on the cluster.
# :::

# %% [markdown]
# (resource_with_overrides)=
#
# ## Using `with_overrides`
#
# ### override Resources
# You can use the `with_overrides` method to override the resources allocated to the tasks dynamically.
# Let's understand how the resources can be initialized with an example.

# %% [markdown]
# Import the dependencies.
# %%
import typing  # noqa: E402

from flytekit import Resources, task, workflow  # noqa: E402


# %% [markdown]
# Define a task and configure the resources to be allocated to it.
# You can use tasks decorated with memory and storage hints like regular tasks in a workflow.
# %%
@task(requests=Resources(cpu="1", mem="200Mi"), limits=Resources(cpu="2", mem="350Mi"))
def count_unique_numbers_1(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# %% [markdown]
# Define a task that computes the square of a number.
# %%
@task
def square_1(x: int) -> int:
    return x * x


# %% [markdown]
# The `with_overrides` method overrides the old resource allocations.
# %%
@workflow
def my_pipeline(x: typing.List[int]) -> int:
    return square_1(x=count_unique_numbers_1(x=x)).with_overrides(limits=Resources(cpu="6", mem="500Mi"))


# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(count_unique_numbers_1(x=[1, 1, 2]))
    print(my_pipeline(x=[1, 1, 2]))

# %% [markdown]
# You can see the memory allocation below. The memory limit is `500Mi` rather than `350Mi`, and the
# CPU limit is 4, whereas it should have been 6 as specified using `with_overrides`.
# This is because the default platform CPU quota for every pod is 4.
#
# :::{figure} https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/core/resource_allocation.png
# :alt: Resource allocated using "with_overrides" method
#
# Resource allocated using "with_overrides" method
# :::
#
# ### override task_config
# Another example for using `with_overrides` method to override the `task_config`.
# In the following we take TF Trainning for example.
# Let’s understand how the TfJob can be initialized and override with an example.
#
# For task_config, refer to the {py:func}`flytekit:flytekit.task` documentation.
#
# Define some necessary functions and dependency.
# For more detail please check [here](https://docs.flyte.org/projects/cookbook/en/latest/auto_examples/kftensorflow_plugin/tf_mnist.html#run-distributed-tensorflow-training).
# In this content we focus on how to override the `task_conf`.
# %%
import os
from dataclasses import dataclass
from typing import NamedTuple, Tuple

from dataclasses_json import dataclass_json
from flytekit import ImageSpec, Resources, dynamic, task, workflow
from flytekit.types.directory import FlyteDirectory

custom_image = ImageSpec(
    name="kftensorflow-flyte-plugin",
    packages=["tensorflow", "tensorflow-datasets", "flytekitplugins-kftensorflow"],
    registry="ghcr.io/flyteorg",
)

if custom_image.is_container():
    import tensorflow as tf
    from flytekitplugins.kftensorflow import PS, Chief, TfJob, Worker

MODEL_FILE_PATH = "saved_model/"


@dataclass_json
@dataclass
class Hyperparameters(object):
    # initialize a data class to store the hyperparameters.
    batch_size_per_replica: int = 64
    buffer_size: int = 10000
    epochs: int = 10


def load_data(
    hyperparameters: Hyperparameters,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.distribute.Strategy]:
    # Fetch train and evaluation datasets
    ...


def get_compiled_model(strategy: tf.distribute.Strategy) -> tf.keras.Model:
    # compile a model
    ...


def decay(epoch: int):
    # define a function for decaying the learning rate
    ...


def train_model(
    model: tf.keras.Model,
    train_dataset: tf.data.Dataset,
    hyperparameters: Hyperparameters,
) -> Tuple[tf.keras.Model, str]:
    # define the train_model function
    ...


def test_model(model: tf.keras.Model, checkpoint_dir: str, eval_dataset: tf.data.Dataset) -> Tuple[float, float]:
    # define the test_model function to evaluate loss and accuracy on the test dataset
    ...


# %% [markdown]
# To create a TensorFlow task, add {py:class}`flytekitplugins:flytekitplugins.kftensorflow.TfJob` config to the Flyte task, that is a plugin can run distributed TensorFlow training on Kubernetes.
# %%
training_outputs = NamedTuple("TrainingOutputs", accuracy=float, loss=float, model_state=FlyteDirectory)

if os.getenv("SANDBOX") != "":
    resources = Resources(gpu="0", mem="1000Mi", storage="500Mi", ephemeral_storage="500Mi")
else:
    resources = Resources(gpu="2", mem="10Gi", storage="10Gi", ephemeral_storage="500Mi")


@task(
    task_config=TfJob(worker=Worker(replicas=1), ps=PS(replicas=1), chief=Chief(replicas=1)),
    retries=2,
    cache=True,
    cache_version="2.2",
    requests=resources,
    limits=resources,
    container_image=custom_image,
)
def mnist_tensorflow_job(hyperparameters: Hyperparameters) -> training_outputs:
    train_dataset, eval_dataset, strategy = load_data(hyperparameters=hyperparameters)
    model = get_compiled_model(strategy=strategy)
    model, checkpoint_dir = train_model(model=model, train_dataset=train_dataset, hyperparameters=hyperparameters)
    eval_loss, eval_accuracy = test_model(model=model, checkpoint_dir=checkpoint_dir, eval_dataset=eval_dataset)
    return training_outputs(accuracy=eval_accuracy, loss=eval_loss, model_state=MODEL_FILE_PATH)


# %% [markdown]
# You can use `@dynamic` to generate tasks at runtime with any custom configurations you want, and `with_overrides` method overrides the old configuration allocations.
# For here we override the worker replica count.
# %%
@workflow
def mnist_tensorflow_workflow(
    hyperparameters: Hyperparameters = Hyperparameters(batch_size_per_replica=64),
) -> training_outputs:
    return mnist_tensorflow_job(hyperparameters=hyperparameters)


@dynamic
def dynamic_run(
    new_worker: int,
    hyperparameters: Hyperparameters = Hyperparameters(batch_size_per_replica=64),
) -> training_outputs:
    return mnist_tensorflow_job(hyperparameters=hyperparameters).with_overrides(
        task_config=TfJob(worker=Worker(replicas=new_worker), ps=PS(replicas=1), chief=Chief(replicas=1))
    )


# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(mnist_tensorflow_workflow())
    print(dynamic_run(new_worker=4))
