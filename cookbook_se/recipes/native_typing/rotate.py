import os
import urllib.request

import cv2
import flytekit
from flytekit import task, workflow
from flytekit.types import FlyteFile

default_images = [
    "https://upload.wikimedia.org/wikipedia/commons/a/a8/Fractal_pyramid.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Mandel_zoom_00_mandelbrot_set.jpg/640px-Mandel_zoom_00_mandelbrot_set.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Julian_fractal.jpg/256px-Julian_fractal.jpg",
]


# TODO: Unit test this - what to do about images?
@task
def rotate(image_location: str) -> FlyteFile:
    """
    Download the given image, rotate it by 180 degrees
    """
    working_dir = flytekit.current_context().working_directory
    local_image = os.path.join(working_dir, "incoming.jpg")
    urllib.request.urlretrieve(image_location, local_image)
    img = cv2.imread(local_image, 0)
    if img is None:
        raise Exception("Failed to read image")
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    mat = cv2.getRotationMatrix2D(center, 180, 1)
    res = cv2.warpAffine(img, mat, (w, h))
    out_path = os.path.join(working_dir, "rotated.jpg")
    cv2.imwrite(out_path, res)
    return FlyteFile(path=out_path)


@workflow
def rotate_one_workflow(in_image: str) -> FlyteFile:
    return rotate(image_location=in_image)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running rotate_one_workflow(in_image=default_images[0]) {rotate_one_workflow(in_image=default_images[0])}"
    )
