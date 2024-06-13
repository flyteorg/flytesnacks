# %% [markdown]
# # Running Distributed Training Using Horovod and MPI
#
# This example demonstrates how to conduct distributed training of a CNN on MNIST data.

# %% [markdown]
# To begin, import the necessary dependencies.
# %%
import pathlib

import flytekit
import tensorflow as tf
from flytekit import Resources, task, workflow
from flytekit.core.base_task import IgnoreOutputs
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.kfmpi import Launcher, MPIJob, Worker


# %% [markdown]
# In the context of this example, we define a training step that will be invoked during the training loop.
# In this step, the training loss is calculated and the model weights are adjusted using gradients.
# %%
@tf.function
def training_step(images, labels, first_batch, mnist_model, loss, opt):
    import horovod.tensorflow as hvd

    with tf.GradientTape() as tape:
        probs = mnist_model(images, training=True)
        loss_value = loss(labels, probs)

    # Add Horovod Distributed GradientTape — a tape that wraps another tf.GradientTape,
    # using an allreduce to combine gradient values before applying gradients to model weights.
    tape = hvd.DistributedGradientTape(tape)

    grads = tape.gradient(loss_value, mnist_model.trainable_variables)
    opt.apply_gradients(zip(grads, mnist_model.trainable_variables))

    # Broadcast initial variable states from rank 0 to all other processes.
    # This is necessary to ensure consistent initialization of all workers when
    # training is started with random weights or restored from a checkpoint.
    #
    # Note: Broadcast should be done after the first gradient step to ensure optimizer
    # initialization.
    if first_batch:
        hvd.broadcast_variables(mnist_model.variables, root_rank=0)
        hvd.broadcast_variables(opt.variables(), root_rank=0)

    return loss_value


# %% [markdown]
# To create an MPI task, add {py:class}`~flytekitplugins.kfmpi.MPIJob` config to the Flyte task.
# The configuration given in the `MPIJob` constructor will be used to set up the distributed training environment.
#
# Broadly, let us define a task that executes the following operations:
#
# 1. Loads the MNIST data
# 2. Prepares the data for training
# 3. Initializes a CNN model
# 4. Invokes the `training_step()` function to train the model
# 5. Saves the model, checkpoint history, and returns the result
#
# :::{note}
# For running Horovod code specifically, an alternative to using the `MPIJob` configuration is to employ the
# [`HorovodJob`](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-kf-mpi/flytekitplugins/kfmpi/task.py#L222)
# configuration. Internally, the `HorovodJob` configuration utilizes the `horovodrun` command,
# while the `MPIJob` configuration utilizes `mpirun`.
# :::
# %%
@task(
    task_config=MPIJob(
        launcher=Launcher(
            replicas=1,
        ),
        worker=Worker(
            replicas=1,
        ),
    ),
    retries=3,
    cache=True,
    cache_version="0.1",
    requests=Resources(cpu="1", mem="1000Mi"),
    limits=Resources(cpu="2"),
)
def horovod_train_task(batch_size: int, buffer_size: int, dataset_size: int) -> FlyteDirectory:
    import horovod.tensorflow as hvd

    hvd.init()

    (mnist_images, mnist_labels), _ = tf.keras.datasets.mnist.load_data(path="mnist-%d.npz" % hvd.rank())

    dataset = tf.data.Dataset.from_tensor_slices(
        (
            tf.cast(mnist_images[..., tf.newaxis] / 255.0, tf.float32),
            tf.cast(mnist_labels, tf.int64),
        )
    )
    dataset = dataset.repeat().shuffle(buffer_size).batch(batch_size)

    mnist_model = tf.keras.Sequential(
        [
            tf.keras.layers.Conv2D(32, [3, 3], activation="relu"),
            tf.keras.layers.Conv2D(64, [3, 3], activation="relu"),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )
    loss = tf.losses.SparseCategoricalCrossentropy()

    # Adjust learning rate based on number of GPUs
    opt = tf.optimizers.Adam(0.001 * hvd.size())

    checkpoint_dir = ".checkpoint"
    pathlib.Path(checkpoint_dir).mkdir(exist_ok=True)

    checkpoint = tf.train.Checkpoint(model=mnist_model, optimizer=opt)

    # Adjust number of steps based on number of GPUs
    for batch, (images, labels) in enumerate(dataset.take(dataset_size // hvd.size())):
        loss_value = training_step(images, labels, batch == 0, mnist_model, loss, opt)

        if batch % 10 == 0 and hvd.local_rank() == 0:
            print("Step #%d\tLoss: %.6f" % (batch, loss_value))

    if hvd.rank() != 0:
        raise IgnoreOutputs("I am not rank 0")

    working_dir = flytekit.current_context().working_directory
    checkpoint_prefix = pathlib.Path(working_dir) / "checkpoint"
    checkpoint.save(checkpoint_prefix)

    tf.keras.models.save_model(
        mnist_model,
        str(working_dir),
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None,
        save_traces=True,
    )
    return FlyteDirectory(path=str(working_dir))


# %% [markdown]
# Lastly, define a workflow.
# %%
@workflow
def horovod_training_wf(batch_size: int = 128, buffer_size: int = 10000, dataset_size: int = 10000) -> FlyteDirectory:
    """
    :param batch_size: Represents the number of consecutive elements of the dataset to combine in a single batch.
    :param buffer_size: Defines the size of the buffer used to hold elements of the dataset used for training.
    :param dataset_size: The number of elements of this dataset that should be taken to form the new dataset when
        running batched training.
    """
    return horovod_train_task(batch_size=batch_size, buffer_size=buffer_size, dataset_size=dataset_size)


# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    model, plot, logs = horovod_training_wf()
    print(f"Model: {model}, plot PNG: {plot}, Tensorboard Log Dir: {logs}")

# %% [markdown]
# :::{note}
# In the context of distributed training, it's important to acknowledge that return values from various workers could potentially vary.
# If you need to regulate which worker's return value gets passed on to subsequent tasks in the workflow,
# you have the option to raise an
# [IgnoreOutputs exception](https://docs.flyte.org/en/latest/api/flytekit/generated/flytekit.core.base_task.IgnoreOutputs.html#flytekit-core-base-task-ignoreoutputs)
# for all remaining ranks.
# :::
# %%
