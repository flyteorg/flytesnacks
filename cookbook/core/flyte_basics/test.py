from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory
import subprocess
import pathlib
import flytekit
import os
from flytekit import Resources


@task
def test_task() -> FlyteDirectory:
    working_dir = flytekit.current_context().working_directory
    data_dir = pathlib.Path(os.path.join(working_dir, "data"))
    data_dir.mkdir(exist_ok=True)

    download_subp = subprocess.run(
        [
            "curl",
            "https://cdn.discordapp.com/attachments/545481172399030272/886952942903627786/rossmann.tgz",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "tar",
            "-xz",
            "-C",
            data_dir,
        ],
        input=download_subp.stdout,
    )
    return FlyteDirectory(path=str(data_dir))


@task(limits=Resources(mem="500Mi"))
def use_directory(directory: FlyteDirectory) -> bool:
    return os.path.isfile(os.path.join(directory, "train.csv"))


@workflow
def wf() -> bool:
    return use_directory(directory=test_task())
