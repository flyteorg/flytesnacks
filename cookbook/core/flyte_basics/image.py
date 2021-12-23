"""
Consume and Produce an image.
"""
import os

import cv2
import flytekit
from flytekit import task, workflow
from flytekit.types.file import JPEGImageFile


@task
def rotate(img: JPEGImageFile) -> JPEGImageFile:
    """
    Download & rotate the image by 180 degrees.
    """
    working_dir = flytekit.current_context().working_directory
    path = img.download()
    img = cv2.imread(path, 0)
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    mat = cv2.getRotationMatrix2D(center, 180, 1)
    res = cv2.warpAffine(img, mat, (w, h))
    out_path = os.path.join(
        working_dir,
        f"rotated-{os.path.basename(path).rsplit('.')[0]}.jpg",
    )
    cv2.imwrite(out_path, res)
    return JPEGImageFile(path=out_path)


@workflow
def wf(
    img: JPEGImageFile = "https://cdn.discordapp.com/attachments/545481172399030272/923516487573065778/Heraldic_tincture.jpg",
) -> JPEGImageFile:
    return rotate(img=img)


if __name__ == "__main__":
    print(wf())
