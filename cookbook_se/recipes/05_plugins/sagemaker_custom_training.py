import typing
from dataclasses import dataclass

import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
from dataclasses_json import dataclass_json
from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from flytekit.taskplugins.sagemaker import SagemakerTrainingJobConfig
from flytekit.models.sagemaker import training_job as training_job_models

HDF5EncodedModelFile = FlyteFile[typing.TypeVar("hdf5")]
TrainingOutputs = typing.NamedTuple("TrainingOutputs", model=HDF5EncodedModelFile, epoch_logs=dict)
PNGImage = FlyteFile[typing.TypeVar("png")]
PlotOutputs = typing.NamedTuple("PlotOutputs", accuracy=PNGImage, loss=PNGImage)


@dataclass_json
@dataclass
class HyperParameters(object):
    epochs: int


def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label


@task(
    task_config=SagemakerTrainingJobConfig(
        algorithm_specification=training_job_models.AlgorithmSpecification(
            input_mode=training_job_models.InputMode.FILE,
            algorithm_name=training_job_models.AlgorithmName.CUSTOM,
            algorithm_version="",
            input_content_type=training_job_models.InputContentType.TEXT_CSV,
        ),
        training_job_resource_config=training_job_models.TrainingJobResourceConfig(
            instance_type="ml.m4.xlarge",
            instance_count=1,
            volume_size_in_gb=25,
        ),
    ),
    cache_version="1.0",
    cache=True,
    container_image="{{.image.sagemaker-tf.fqn}}:{{.image.default.version}}"
)
def custom_training_task(hyper_params: HyperParameters) -> TrainingOutputs:
    (ds_train, ds_test), ds_info = tfds.load(
        'mnist',
        split=['train', 'test'],
        shuffle_files=True,
        as_supervised=True,
        with_info=True,
    )

    ds_train = ds_train.map(
        normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_train = ds_train.cache()
    ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
    ds_train = ds_train.batch(128)
    ds_train = ds_train.prefetch(tf.data.experimental.AUTOTUNE)

    ds_test = ds_test.map(
        normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_test = ds_test.batch(128)
    ds_test = ds_test.cache()
    ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    history = model.fit(
        ds_train,
        epochs=hyper_params.epochs,
        validation_data=ds_test,
    )

    serialized_model = "my_model.h5"
    model.save(serialized_model, overwrite=True)

    return TrainingOutputs(model=HDF5EncodedModelFile(serialized_model), epoch_logs=history.history)


@task
def plot_loss_and_accuracy(epoch_logs: dict) -> PlotOutputs:
    # summarize history for accuracy
    plt.plot(epoch_logs['sparse_categorical_accuracy'])
    plt.plot(epoch_logs['val_sparse_categorical_accuracy'])
    plt.title('Sparse Categorical accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    accuracy_plot = "accuracy.png"
    plt.savefig(accuracy_plot)
    # summarize history for loss
    plt.plot(epoch_logs['loss'])
    plt.plot(epoch_logs['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    loss_plot = "loss.png"
    plt.savefig(loss_plot)

    return PlotOutputs(accuracy=FlyteFile(accuracy_plot), loss=FlyteFile(loss_plot))


@workflow
def mnist_trainer(hyper_params: HyperParameters) -> (HDF5EncodedModelFile, PNGImage, PNGImage):
    model, history = custom_training_task(hyper_params=hyper_params)
    accuracy, loss = plot_loss_and_accuracy(epoch_logs=history)
    return model, accuracy, loss


if __name__ == "__main__":
    print(mnist_trainer(hyper_params=HyperParameters(epochs=6)))
