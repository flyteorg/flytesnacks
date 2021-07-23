import os
from typing import List

from flytekit import task, workflow, dynamic
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile


@task
def file_task(ff: FlyteFile) -> List[str]:
    return ["Hello", "world", f"{ff}"]


@dynamic
def search_execution(folder: FlyteDirectory) -> List[List[str]]:
    ffs = []
    for file in [os.path.join(folder, f) for f in os.listdir(folder)]:
        ffs.append(file_task(ff=file))

    return ffs
