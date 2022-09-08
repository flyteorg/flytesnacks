import typing
import tempfile

import os

from flytekit import task, workflow
from flytekit.types.file import FlyteFile


@task
def files_task() -> typing.Tuple[FlyteFile, FlyteFile, FlyteFile]:
    fd, filename1 = tempfile.mkstemp()
    with os.fdopen(fd, "w") as tmp:
        tmp.write("hello world 1")

    fd, filename2 = tempfile.mkstemp()
    with os.fdopen(fd, "w") as tmp:
        tmp.write("hello world 2")

    fd, filename3 = tempfile.mkstemp()
    with os.fdopen(fd, "w") as tmp:
        tmp.write("hello world 3")

    print(f"File 1: {filename1} File 2: {filename2} File 3: {filename3}")

    return filename1, FlyteFile(filename2), FlyteFile(filename3,
                                                      remote_path="s3://union-opencompute-open-compute2-playground/yt/specific_file_location_1")


@workflow
def files_wf() -> typing.Tuple[FlyteFile, FlyteFile, FlyteFile]:
    return files_task()
