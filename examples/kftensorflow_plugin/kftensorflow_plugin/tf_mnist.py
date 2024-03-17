# %% [markdown]
# # Run Distributed TensorFlow Training
#
# When you need to scale up model training using TensorFlow, you can utilize the
# {py:class}`~tensorflow:tf.distribute.Strategy` to distribute your training across multiple devices.
# Several strategies are available within this API, all of which can be employed as needed.
# In this example, we employ the {py:class}`~tensorflow:tf.distribute.MirroredStrategy` to train an MNIST model using a CNN.
#
# The `MirroredStrategy` enables synchronous distributed training across multiple GPUs on a single machine.
# For a deeper understanding of distributed training with TensorFlow, refer to the
# [distributed training with TensorFlow](https://www.tensorflow.org/guide/distributed_training) in the TensorFlow documentation.
#
# To begin, load the libraries.
# %%
import os
from dataclasses import dataclass
from typing import NamedTuple, Tuple

from dataclasses_json import dataclass_json
from flytekit import ImageSpec, Resources, task, workflow
from flytekit.types.directory import FlyteDirectory

# %% [markdown]
# Create an `ImageSpec` to encompass all the dependencies needed for the TensorFlow task.
# %%
custom_image = ImageSpec(
    name="kftensorflow-flyte-plugin",
    packages=["tensorflow", "tensorflow-datasets", "flytekitplugins-kftensorflow"],
    registry="ghcr.io/flyteorg",
)

# %% [markdown]
# :::{important}
# Replace `ghcr.io/flyteorg` with a container registry you've access to publish to.
# To upload the image to the local registry in the demo cluster, indicate the registry as `localhost:30000`.
# :::
#
# The following imports are required to configure the TensorFlow cluster in Flyte.
# You can load them on demand.
# %%
if custom_image.is_container():
    import tensorflow as tf
    import tensorflow_datasets as tfds
    from flytekitplugins.kftensorflow import PS, Chief, TfJob, Worker

# %% [markdown]
# You can activate GPU support by either using the base image that includes the necessary GPU dependencies
# or by initializing the [CUDA parameters](https://github.com/flyteorg/flytekit/blob/master/flytekit/image_spec/image_spec.py#L34-L35)
# within the `ImageSpec`.
#
# For this example, we define the `MODEL_FILE_PATH` variable to indicate the storage location for the model file.
# %%
MODEL_FILE_PATH = "saved_model/"


# %% [markdown]
# We initialize a data class to store the hyperparameters.
# %%
@dataclass_json
@dataclass
class Hyperparameters(object):
    batch_size_per_replica: int = 64
    buffer_size: int = 10000
    epochs: int = 10


# %% [markdown]
# We use the [MNIST](https://www.tensorflow.org/datasets/catalog/mnist) dataset to train our model.
# %%
def load_data(
    hyperparameters: Hyperparameters,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.distribute.Strategy]:
    datasets, _ = tfds.load(name="mnist", with_info=True, as_supervised=True)
    mnist_train, mnist_test = datasets["train"], datasets["test"]

    strategy = tf.distribute.MirroredStrategy()
    print("Number of devices: {}".format(strategy.num_replicas_in_sync))

    # strategy.num_replicas_in_sync returns the number of replicas; helpful to utilize the extra compute power by increasing the batch size
    BATCH_SIZE = hyperparameters.batch_size_per_replica * strategy.num_replicas_in_sync

    def scale(image, label):
        image = tf.cast(image, tf.float32)
        image /= 255

        return image, label

    # Fetch train and evaluation datasets
    train_dataset = mnist_train.map(scale).shuffle(hyperparameters.buffer_size).batch(BATCH_SIZE)
    eval_dataset = mnist_test.map(scale).batch(BATCH_SIZE)

    return train_dataset, eval_dataset, strategy


# %% [markdown]
# We create and compile a model in the context of [Strategy.scope](https://www.tensorflow.org/api_docs/python/tf/distribute/MirroredStrategy#scope).
# %%
def get_compiled_model(strategy: tf.distribute.Strategy) -> tf.keras.Model:
    with strategy.scope():
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Conv2D(32, 3, activation="relu", input_shape=(28, 28, 1)),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(10),
            ]
        )

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer=tf.keras.optimizers.Adam(),
            metrics=["accuracy"],
        )

    return model


# %% [markdown]
# We define a function for decaying the learning rate.
# %%
def decay(epoch: int):
    if epoch < 3:
        return 1e-3
    elif epoch >= 3 and epoch < 7:
        return 1e-4
    else:
        return 1e-5


# %% [markdown]
# We define the `train_model` function to initiate model training with three callbacks:
#
# - {py:class}`~tensorflow:tf.keras.callbacks.TensorBoard` to log the training metrics
# - {py:class}`~tensorflow:tf.keras.callbacks.ModelCheckpoint` to save the model after every epoch
# - {py:class}`~tensorflow:tf.keras.callbacks.LearningRateScheduler` to decay the learning rate
# %%
def train_model(
    model: tf.keras.Model,
    train_dataset: tf.data.Dataset,
    hyperparameters: Hyperparameters,
) -> Tuple[tf.keras.Model, str]:
    # Define the checkpoint directory to store checkpoints
    checkpoint_dir = "./training_checkpoints"

    # Define the name of the checkpoint files
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    # Define a callback for printing the learning rate at the end of each epoch
    class PrintLR(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            print("\nLearning rate for epoch {} is {}".format(epoch + 1, model.optimizer.lr.numpy()))

    # Put all the callbacks together
    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir="./logs"),
        tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix, save_weights_only=True),
        tf.keras.callbacks.LearningRateScheduler(decay),
        PrintLR(),
    ]

    # Train the model
    model.fit(train_dataset, epochs=hyperparameters.epochs, callbacks=callbacks)

    # Save the model
    model.save(MODEL_FILE_PATH, save_format="tf")

    return model, checkpoint_dir


# %% [markdown]
# We define the `test_model` function to evaluate loss and accuracy on the test dataset.
# %%
def test_model(model: tf.keras.Model, checkpoint_dir: str, eval_dataset: tf.data.Dataset) -> Tuple[float, float]:
    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

    eval_loss, eval_acc = model.evaluate(eval_dataset)

    return eval_loss, eval_acc


# %% [markdown]
# To create a TensorFlow task, add {py:class}`~flytekitplugins.kftensorflow.TfJob` config to the Flyte task.
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
# The task is initiated using `TFJob` with specific values configured:
#
# - `num_workers`: specifies the number of worker replicas to be launched in the cluster for this job
# - `num_ps_replicas`: determines the count of parameter server replicas to utilize
# - `num_chief_replicas`: defines the number of chief replicas to be employed
#
# For our example, with `MirroredStrategy` leveraging an all-reduce algorithm to communicate variable updates across devices,
# the parameter `num_ps_replicas` does not hold significance.
#
# :::{note}
# If you're interested in exploring the diverse TensorFlow strategies available for distributed training,
# you can find comprehensive information in the
# [types of strategies](https://www.tensorflow.org/guide/distributed_training#types_of_strategies)
# section of the TensorFlow documentation.
# :::
#
# Lastly, define a workflow to invoke the tasks.
# %%
@workflow
def mnist_tensorflow_workflow(
    hyperparameters: Hyperparameters = Hyperparameters(batch_size_per_replica=64),
) -> training_outputs:
    return mnist_tensorflow_job(hyperparameters=hyperparameters)


# %% [markdown]
# You can run the code locally.
# %%
if __name__ == "__main__":
    print(mnist_tensorflow_workflow())

# %% [markdown]
# :::{note}
# In the context of distributed training, it's important to acknowledge that return values from various workers could potentially vary.
# If you need to regulate which worker's return value gets passed on to subsequent tasks in the workflow,
# you have the option to raise an
# [IgnoreOutputs exception](https://docs.flyte.org/en/latest/api/flytekit/generated/flytekit.core.base_task.IgnoreOutputs.html#flytekit-core-base-task-ignoreoutputs)
# for all remaining ranks.
# :::
