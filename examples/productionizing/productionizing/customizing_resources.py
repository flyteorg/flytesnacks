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

from typing import NamedTuple

import tensorflow as tf

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
# To create a TensorFlow task, add {py:class}`flytekitplugins:flytekitplugins.kftensorflow.TfJob` config to the Flyte task, that is a plugin can run distributed TensorFlow training on Kubernetes.
# %%
from flytekit import Resources, dynamic, task, workflow
from flytekitplugins.kftensorflow import PS, Chief, TfJob, Worker

TrainingOutputs = NamedTuple(
    "TrainingOutputs",
    [
        ("model", tf.keras.Model),
        ("accuracy", float),
        ("loss", float),
    ],
)


@task(
    task_config=TfJob(worker=Worker(replicas=1), ps=PS(replicas=1), chief=Chief(replicas=1)),
    cache_version="1.0",
    cache=True,
    requests=Resources(cpu="1", mem="2048Mi"),
    limits=Resources(cpu="1", mem="2048Mi"),
)
def train_model() -> TrainingOutputs:
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
    X_train, X_test = X_train / 255.0, X_test / 255.0
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(10),
            ]
        )
        model.compile(
            optimizer="adam", loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"]
        )
        BATCH_SIZE = 64
        NUM_EPOCHS = 5
        model.fit(X_train, y_train, epochs=NUM_EPOCHS, batch_size=BATCH_SIZE)
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=2)

    return TrainingOutputs(model=model, accuracy=test_accuracy, loss=test_loss)


# %% [markdown]
# You can use `@dynamic` to generate tasks at runtime with any custom configurations you want, and `with_overrides` method overrides the old configuration allocations.
# For here we override the worker replica count.
# %%
@workflow
def my_tensorflow_workflow() -> TrainingOutputs:
    return train_model()


@dynamic
def dynamic_run(new_worker: int) -> TrainingOutputs:
    return train_model().with_overrides(
        task_config=TfJob(worker=Worker(replicas=new_worker), ps=PS(replicas=1), chief=Chief(replicas=1))
    )


# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(my_tensorflow_workflow())
    print(dynamic_run(new_worker=4))
