# Import necessary libraries and modules

import tensorflow as tf
from flytekit import task, workflow
from flytekit.types.directory import TFRecordsDirectory
from flytekit.types.file import TFRecordFile


# TensorFlow Model
@task
def train_model() -> tf.keras.Model:
    model = tf.keras.Sequential(
        [tf.keras.layers.Dense(128, activation="relu"), tf.keras.layers.Dense(10, activation="softmax")]
    )
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


@task
def evaluate_model(model: tf.keras.Model, x: tf.Tensor, y: tf.Tensor) -> float:
    loss, accuracy = model.evaluate(x, y)
    return accuracy


@workflow
def training_workflow(x: tf.Tensor, y: tf.Tensor) -> float:
    model = train_model()
    return evaluate_model(model=model, x=x, y=y)


# TFRecord Files
@task
def process_tfrecord(file: TFRecordFile) -> int:
    count = 0
    for record in tf.data.TFRecordDataset(file):
        count += 1
    return count


@workflow
def tfrecord_workflow(file: TFRecordFile) -> int:
    return process_tfrecord(file=file)


# TFRecord Directories
@task
def process_tfrecords_dir(dir: TFRecordsDirectory) -> int:
    count = 0
    for record in tf.data.TFRecordDataset(dir.path):
        count += 1
    return count


@workflow
def tfrecords_dir_workflow(dir: TFRecordsDirectory) -> int:
    return process_tfrecords_dir(dir=dir)
