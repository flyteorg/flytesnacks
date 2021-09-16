import tensorflow as tf
import horovod.tensorflow as hvd
import numpy as np
from tensorflow import keras
from flytekit.core.base_task import IgnoreOutputs
from flytekitplugins.kfmpi import MPIJob

layers = tf.layers

tf.logging.set_verbosity(tf.logging.INFO)

@dataclass_json
@dataclass
class Hyperparameters:
    batch_size: int = 100
    learning_rate: float = 0.0001
    epochs: int = 100
    local_checkpoint_file: str = "checkpoint"


def conv_model(feature, target, mode):
    """2-layer convolution model."""
    # Convert the target to a one-hot tensor of shape (batch_size, 10) and
    # with a on-value of 1 for each one-hot vector of length 10.
    target = tf.one_hot(tf.cast(target, tf.int32), 10, 1, 0)

    # Reshape feature to 4d tensor with 2nd and 3rd dimensions being
    # image width and height final dimension being the number of color channels.
    feature = tf.reshape(feature, [-1, 28, 28, 1])

    # First conv layer will compute 32 features for each 5x5 patch
    with tf.variable_scope('conv_layer1'):
        h_conv1 = layers.conv2d(feature, 32, kernel_size=[5, 5],
                                activation=tf.nn.relu, padding="SAME")
        h_pool1 = tf.nn.max_pool(
            h_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # Second conv layer will compute 64 features for each 5x5 patch.
    with tf.variable_scope('conv_layer2'):
        h_conv2 = layers.conv2d(h_pool1, 64, kernel_size=[5, 5],
                                activation=tf.nn.relu, padding="SAME")
        h_pool2 = tf.nn.max_pool(
            h_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # reshape tensor into a batch of vectors
        h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])

    # Densely connected layer with 1024 neurons.
    h_fc1 = layers.dropout(
        layers.dense(h_pool2_flat, 1024, activation=tf.nn.relu),
        rate=0.5, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Compute logits (1 per class) and compute loss.
    logits = layers.dense(h_fc1, 10, activation=None)
    loss = tf.losses.softmax_cross_entropy(target, logits)

    return tf.argmax(logits, 1), loss


def train_input_generator(x_train, y_train, batch_size=64):
    assert len(x_train) == len(y_train)
    while True:
        p = np.random.permutation(len(x_train))
        x_train, y_train = x_train[p], y_train[p]
        index = 0
        while index <= len(x_train) - batch_size:
            yield x_train[index:index + batch_size], \
                y_train[index:index + batch_size],
            index += batch_size


@task(
    task_config=MPIJob(
        num_workers=2,
        num_launcher_replicas=1,
        slots=1,
    ),
    retries=5,
    cache=True,
    cache_version="1.0",
    per_replica_requests=Resources(
        cpu="1", mem="30Gi", storage="20Gi", ephemeral_storage="500Mi"
    ),
    per_replica_limits=Resources(
        cpu="1", mem="30Gi", storage="20Gi", ephemeral_storage="500Mi"
    ),
)
def horovod_train_task(
    hp: Hyperparameters
) -> (FlyteFile):
    # Horovod: initialize Horovod.
    hvd.init()

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data('MNIST-data-%d' % hvd.rank())

    # The shape of downloaded data is (-1, 28, 28), hence we need to reshape it
    # into (-1, 784) to feed into our network. Also, need to normalize the
    # features between 0 and 1.
    x_train = np.reshape(x_train, (-1, 784)) / 255.0
    x_test = np.reshape(x_test, (-1, 784)) / 255.0

    # Build model...
    with tf.name_scope('input'):
        image = tf.placeholder(tf.float32, [None, 784], name='image')
        label = tf.placeholder(tf.float32, [None], name='label')
    predict, loss = conv_model(image, label, tf.estimator.ModeKeys.TRAIN)

    lr_scaler = hvd.size()
    # By default, Adasum doesn't need scaling when increasing batch size. If used with NCCL,
    # scale lr by local_size
    if hp.use_adasum:
        lr_scaler = hvd.local_size() if hvd.nccl_built() else 1

    # Horovod: adjust learning rate based on lr_scaler.
    opt = tf.train.AdamOptimizer(hp.learning_rate * lr_scaler)

    # Horovod: add Horovod Distributed Optimizer.
    opt = hvd.DistributedOptimizer(opt, op=hvd.Adasum if hp.use_adasum else hvd.Average)

    global_step = tf.train.get_or_create_global_step()
    train_op = opt.minimize(loss, global_step=global_step)

    hooks = [
        # Horovod: BroadcastGlobalVariablesHook broadcasts initial variable states
        # from rank 0 to all other processes. This is necessary to ensure consistent
        # initialization of all workers when training is started with random weights
        # or restored from a checkpoint.
        hvd.BroadcastGlobalVariablesHook(0),

        # Horovod: adjust number of steps based on number of GPUs.
        tf.train.StopAtStepHook(last_step=hp.num_steps // hvd.size()),

        tf.train.LoggingTensorHook(tensors={'step': global_step, 'loss': loss},
                                   every_n_iter=10),
    ]
    # Horovod: pin GPU to be used to process local rank (one GPU per process)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.visible_device_list = str(hvd.local_rank())

    # Horovod: save checkpoints only on worker 0 to prevent other workers from
    # corrupting them.
    checkpoint_dir = hp.local_checkpoint_file if hvd.rank() == 0 else None

    training_batch_generator = train_input_generator(x_train,
                                                     y_train, batch_size=hp.batch_size)
    # The MonitoredTrainingSession takes care of session initialization,
    # restoring from a checkpoint, saving to a checkpoint, and closing when done
    # or an error occurs.
    with tf.train.MonitoredTrainingSession(checkpoint_dir=checkpoint_dir,
                                           hooks=hooks,
                                           config=config) as mon_sess:
        while not mon_sess.should_stop():
            # Run a training step synchronously.
            image_, label_ = next(training_batch_generator)
            mon_sess.run(train_op, feed_dict={image: image_, label: label_})

    if hvd.rank() != 0:
        raise IgnoreOutputs("I am not rank 0")
    else:
        return checkpoint_dir


@workflow
def horovod_training_wf(
    hp: Hyperparameters = Hyperparameters(),
) -> (FlyteFile):
    return horovod_train_task(
        hp=hp
    )
