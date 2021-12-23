"""
Array of images from map task.
"""
import os
from typing import List

import cv2
import flytekit
from flytekit import map_task, task, workflow
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
    images: List[JPEGImageFile] = [
        "https://cdn.discordapp.com/attachments/545481172399030272/923516487573065778/Heraldic_tincture.jpg",
        "https://cdn.discordapp.com/attachments/545481172399030272/923516487296233472/Hummingbird.jpg",
        "https://cdn.discordapp.com/attachments/545481172399030272/923516487094894622/Grecia._Le_radici_della_Civilta_Europea_photobook_by_Pino_Musi.jpg",
        "https://cdn.discordapp.com/attachments/545481172399030272/923516486797107210/640px-Dulmen_Wildpark_--_2020_--_3427.jpg",
        "https://cdn.discordapp.com/attachments/545481172399030272/923516486545461267/640px-All_Gizah_Pyramids.jpg",
    ],
) -> List[JPEGImageFile]:
    return map_task(rotate)(img=images)


if __name__ == "__main__":
    print(wf())
