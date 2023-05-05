"""
.. _image_spec_example:

Building Image without Dockerfile
---------------------------------

.. tags:: Containerization, Intermediate

Image Spec is a way to specify how to build a container image without a Dockerfile. The image spec by default will be
converted to an `Envd <https://envd.tensorchord.ai/>`__ config, and the `Envd builder
<https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-envd/flytekitplugins/envd
/image_builder.py#L12-L34>`__ will build the image for you. However, you can also register your own builder to build
the image using other tools.

For every :py:class:`flytekit.PythonFunctionTask` task or a task decorated with the ``@task`` decorator,
you can specify rules for binding container images. By default, flytekit binds a single container image, i.e.,
the `default Docker image <https://ghcr.io/flyteorg/flytekit>`__, to all tasks. To modify this behavior,
use the ``container_image`` parameter available in the :py:func:`flytekit.task` decorator, and pass an
`ImageSpec`.

Before building the image, Flytekit checks the container registry first to see if the image already exists. By doing
so, it avoids having to rebuild the image over and over again. If the image does not exist, flytekit will build the
image before registering the workflow, and replace the image name in the task template with the newly built image name.

"""
# %%
# .. admonition:: Prerequisites
#    :class: important
#
#    - Install `flytekitplugins-envd <https://github.com/flyteorg/flytekit/tree/master/plugins/flytekit-envd>`__ to build the image spec.
#    - To build the image on remote machine, check this `doc <https://envd.tensorchord.ai/teams/context.html#start-remote-buildkitd-on-builder-machine>`__
#
#
import pandas as pd
from flytekit import ImageSpec, task, workflow

# %%
# Image Spec
# ==========
#
# People can specify python packages, apt packages, and environment variables. Those packages will be added on top of
# the `default image <https://github.com/flyteorg/flytekit/blob/master/Dockerfile>`__. You can also override the
# default image by passing ``base_image`` parameter to the ``ImageSpec``.
pandas_image_spec = ImageSpec(
    base_image="ghcr.io/flyteorg/flytekit:py3.8-1.6.0a1",
    packages=["pandas", "numpy"],
    python_version="3.9",
    apt_packages=["git"],
    env={"Debug": "True"},
    registry="pingsutw",
)

tensorflow_image_spec = ImageSpec(base_image="ghcr.io/flyteorg/flytekit:py3.8-1.6.0a1", packages=["tensorflow"], registry="pingsutw")

# %%
# ``is_container`` is used to check if the task is using the image built from the image spec.
# If the task is using the image built from the image spec, then the task will import tensorflow.
# It can reduce module loading time and avoid unnecessary dependency installation in the single image.
# if tensorflow_image_spec.is_container():  # TODO: cut a beta release
import tensorflow as tf


# %%
# Both ``get_pandas_dataframe`` and ``train_model`` will use the image built from the image spec.
@task(container_image=pandas_image_spec)
def get_pandas_dataframe() -> (pd.DataFrame, pd.Series):
    df = pd.read_csv("https://storage.googleapis.com/download.tensorflow.org/data/heart.csv")
    print(df.head())
    return df[['age', 'thalach', 'trestbps',  'chol', 'oldpeak']], df.pop('target')


# %%
# Get a basic model to train.
@task(container_image=tensorflow_image_spec)
def get_model(layers: int, feature: pd.DataFrame) -> tf.keras.Model:
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(feature)

    model = tf.keras.Sequential([
        normalizer,
        tf.keras.layers.Dense(layers, activation='relu'),
        tf.keras.layers.Dense(layers, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model


# %%
# Users can also pass imageSpec yaml file to the ``pyflyte run`` or ``pyflyte register`` command to override the
# container_image. For instance:
#
# .. code-block:: yaml
#
#    # imageSpec.yaml
#    python_version: 3.11
#    registry: pingsutw
#    packages:
#      - tensorflow
#    env:
#      Debug: "True"
#
#
# .. code-block::
#
#    # Use pyflyte to register the workflow
#    pyflyte run --remote --image image.yaml image_spec_example.py wf
#
@task(container_image=tensorflow_image_spec)
def train_model(model: tf.keras.Model, feature: pd.DataFrame, target: pd.Series) -> tf.keras.Model:
    model.fit(feature, target, epochs=3, batch_size=100)
    return model


# %%
# A simple pipeline to train a model.
@workflow()
def wf():
    feature, target = get_pandas_dataframe()
    model = get_model(layers=10, feature=feature)
    train_model(model=model, feature=feature, target=target)


if __name__ == "__main__":
    wf()
