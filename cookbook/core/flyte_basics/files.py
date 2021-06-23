"""
Working With Files
-------------------

Files are one of the most fundamental entities that users of Python work with, and they are fully supported by Flyte.
In the IDL, they are known as `Blob <https://github.com/lyft/flyteidl/blob/cee566b2e6e109120f1bb34c980b1cfaf006a473/protos/flyteidl/core/literals.proto#L33>`__ literals
which are backed by the `blob type <https://github.com/lyft/flyteidl/blob/cee566b2e6e109120f1bb34c980b1cfaf006a473/protos/flyteidl/core/types.proto#L47>`__.

Let's assume our mission here is pretty simple. We want to consider a couple of links, download the pictures, rotate them, and return the rotated images.
"""

# %%
# Let's first import the libraries.
import os

import cv2
import flytekit
from flytekit import task, workflow
from flytekit.types.file import JPEGImageFile

# %%
# ``JPEGImageFile`` is a pre-formatted FlyteFile type. It is equivalent to ``FlyteFile[typing.TypeVar("jpeg")]``.
#
# .. note::
#   ``FlyteFile`` literal can be scoped with a string, which gets inserted into the format of the Blob type ("jpeg" is the string in ``FlyteFile[typing.TypeVar("jpeg")]``). The ``[]`` are entirely optional, and if you don't specify it, the format will just be an ``""``.


# %%
# Next, we write a task that accepts a ``JPEGImageFile`` as an input and returns the rotated image as an output, which again is the ``JPEGImageFile``.
# Files do not have a native object in Python, so we had to write one ourselves.
# There does exist the ``os.PathLike`` protocol, but nothing implements it.
@task
def rotate(image_location: JPEGImageFile) -> JPEGImageFile:
    """
    Download the given image, rotate it by 180 degrees
    """
    working_dir = flytekit.current_context().working_directory
    with open(image_location, "rb"):
        ...
    img = cv2.imread(str(image_location), 0)
    if img is None:
        raise Exception("Failed to read image")
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    mat = cv2.getRotationMatrix2D(center, 180, 1)
    res = cv2.warpAffine(img, mat, (w, h))
    out_path = os.path.join(
        working_dir,
        f"rotated-{os.path.basename(image_location.path).rsplit('.')[0]}.jpg",
    )
    cv2.imwrite(out_path, res)
    return JPEGImageFile(path=out_path)


# %%
# When the image URL is sent to the task, the Flytekit engine translates it into a ``FlyteFile`` object on the local drive (but not download it).
# The act of opening it should trigger the download, since FlyteFile does lazy downloading. Moreover, the file name is maintained on download.
#
# Next, we convert ``_SpecificFormatClass`` to string to enable OpenCV to read the file.
#
# When this task finishes, the Flytekit engine returns the ``FlyteFile`` instance, finds a location
# in Flyte's object store (usually S3), uploads the file to that location and creates a Blob literal pointing to it.
#
# .. tip::
#
#   The ``rotate`` task works with ``FlyteFile``, too. However, ``JPEGImageFile`` helps attach the content information.

# %%
# We now define the workflow to call the task.
@workflow
def rotate_one_workflow(in_image: JPEGImageFile) -> JPEGImageFile:
    return rotate(image_location=in_image)


# %%
# Finally, let's execute it!
if __name__ == "__main__":
    default_images = [
        "https://upload.wikimedia.org/wikipedia/commons/a/a8/Fractal_pyramid.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Julian_fractal.jpg/256px-Julian_fractal.jpg",
    ]
    print(f"Running {__file__} main...")
    for index, each_image in enumerate(default_images):
        print(
            f"Running rotate_one_workflow(in_image=default_images[{index}]) {rotate_one_workflow(in_image=each_image)}"
        )
