import os
from dataclasses import dataclass

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import math
import tensorflow as tf
import horovod.keras as hvd
import flytekit


from flytekit import task, workflow, Resources
from flytekit.types.directory import FlyteDirectory
from flytekit.core.base_task import IgnoreOutputs
from flytekitplugins.kfmpi import MPIJob


@dataclass
class ModelScore:
    loss: float
    accuracy: float


@task(
    task_config=MPIJob(
        num_workers=2,
        num_launcher_replicas=1,
        slots=1,
        per_replica_requests=Resources(mem="3000Mi", cpu="1"),
        per_replica_limits=Resources(mem="3000Mi", cpu="1"),
    ),
    retries=5,
    # cache=True,
    # cache_version="0.4",
)
def train(batch_size: int, num_classes: int) -> FlyteDirectory:
    """
    :param batch_size: Represents the number of consecutive elements of this dataset to combine in a single batch.
    :param num_classes: The total number of classes
    """
    # Horovod: initialize Horovod.
    hvd.init()

    # Horovod: pin GPU to be used to process local rank (one GPU per process)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.visible_device_list = str(hvd.local_rank())
    K.set_session(tf.Session(config=config))

    # Horovod: adjust number of epochs based on number of GPUs.
    epochs = int(math.ceil(12.0 / hvd.size()))

    # Input image dimensions
    img_rows, img_cols = 28, 28

    # The data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # Convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    # Horovod: adjust learning rate based on number of GPUs.
    opt = keras.optimizers.Adadelta(1.0 * hvd.size())

    # Horovod: add Horovod Distributed Optimizer.
    opt = hvd.DistributedOptimizer(opt)

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=opt,
                  metrics=['accuracy'])

    callbacks = [
        # Horovod: broadcast initial variable states from rank 0 to all other processes.
        # This is necessary to ensure consistent initialization of all workers when
        # training is started with random weights or restored from a checkpoint.
        hvd.callbacks.BroadcastGlobalVariablesCallback(0),
    ]

    working_dir = flytekit.current_context().working_directory
    working_dir_path = str(working_dir)

    # Horovod: save checkpoints only on worker 0 to prevent other workers from corrupting them.
    if hvd.rank() == 0:
        callbacks.append(keras.callbacks.ModelCheckpoint(working_dir_path+'/checkpoint-{epoch}.h5'))

    model.fit(x_train, y_train,
              batch_size=batch_size,
              callbacks=callbacks,
              epochs=epochs,
              verbose=1 if hvd.rank() == 0 else 0,
              validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test loss: {score[0]}, with type {type(score[0])}")
    print(f"Test accuracy: {score[1]}, with type {type(score[1])}")

    model.save(os.path.join(working_dir_path), "mnist_model")

    return FlyteDirectory(path=working_dir_path)


@workflow
def horovod_training_wf_demo(batch_size: int = 128, num_classes: int = 10) -> FlyteDirectory:
    """
    :param batch_size: Represents the number of consecutive elements of this dataset to combine in a single batch.
    :param num_classes: The total number of classes
    """
    model_dir = train(batch_size=batch_size, num_classes=num_classes)
    return model_dir
