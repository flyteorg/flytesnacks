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
image before registering the workflow, and replace the image name in the workflow spec with the newly built image name.

"""
# %%
# .. admonition:: Prerequisites
#    :class: important
#
#    Install `flytekitplugins-envd <https://github.com/flyteorg/flytekit/tree/master/plugins/flytekit-envd>`__ to build
#    the image spec.
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
image_spec = ImageSpec(
    packages=["pandas", "numpy"],
    python_version="3.9",
    apt_packages=["git"],
    env={"Debug": "True"},
    registry="pingsutw",
)


# %%
# Both ``t1`` and ``t2`` will use the image built from the image spec.
@task(container_image=image_spec)
def t1():
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    print(df)


@task(container_image=image_spec)
def t2():
    print("hello")


# %%
# ``t3`` doesn't specify image_spec, so it will use the default image.
# You can also pass imageSpec yaml file to the ``pyflyte run`` or ``pyflyte register`` command to override it.
# For instance:
#
# .. code-block:: yaml
#
#    # imageSpec.yaml
#    python_version: 3.11
#    packages:
#      - pandas
#      - numpy
#    apt_packages:
#      - git
#    env:
#      Debug: "True"
#
#
# .. code-block::
#
#    # Use pyflyte to register the workflow
#    pyflyte run --remote --image image.yaml image_spec_example.py wf
#
@task()
def t3():
    print("flyte")


@workflow()
def wf():
    t1()
    t2()
    t3()


if __name__ == "__main__":
    wf()
