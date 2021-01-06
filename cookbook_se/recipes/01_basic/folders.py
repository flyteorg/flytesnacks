"""
11: Work with folders
---------------------

Please also see the entry on files. After files, folders are the next fundamental grouping users might find themselves working with. Flyte's IDL supports folders as what we call a multi

"""
import pathlib
import os
import urllib.request

import cv2
import flytekit
from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory


# %%
# Playing on the same example used in the File chapter, this first task downloads a bunch of files into a directory,
# and then returns a Flyte object referencing them.
default_images = [
    "https://upload.wikimedia.org/wikipedia/commons/a/a8/Fractal_pyramid.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Julian_fractal.jpg/256px-Julian_fractal.jpg",
]


@task
def download_files() -> FlyteDirectory:
    """
    Download the given image, rotate it by 180 degrees
    """

    working_dir = flytekit.current_context().working_directory
    pp = pathlib.Path(os.path.join(working_dir, "images"))
    pp.mkdir(exist_ok=True)
    print(f"Writing to {pp}")
    for idx, remote_location in enumerate(default_images):
        local_image = os.path.join(working_dir, "images", f"image_{idx}.jpg")
        urllib.request.urlretrieve(remote_location, local_image)

    return FlyteDirectory(path=os.path.join(working_dir, "images"))


def rotate(local_image: str):
    """
    In place rotation of the image
    """
    print(f"Reading {local_image}!")
    img = cv2.imread(local_image, 0)
    if img is None:
        raise Exception("Failed to read image")
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    mat = cv2.getRotationMatrix2D(center, 180, 1)
    res = cv2.warpAffine(img, mat, (w, h))
    # out_path = os.path.join(working_dir, "rotated.jpg")
    cv2.imwrite(local_image, res)


@task
def rotate_all(img_dir: FlyteDirectory) -> FlyteDirectory:
    """
    Download the given image, rotate it by 180 degrees
    """
    for img in [os.path.join(img_dir, x) for x in os.listdir(img_dir)]:
        rotate(img)
    return FlyteDirectory(path=img_dir.path)


@workflow
def download_and_rotate() -> FlyteDirectory:
    directory = download_files()
    return rotate_all(img_dir=directory)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running main {download_and_rotate()}"
    )
