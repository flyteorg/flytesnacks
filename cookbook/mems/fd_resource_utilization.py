# =========== DEBUG FlyteDirectory resource utilization under flytekit 1.5+ ====================
#
# Begining with flytekit 1.5, we noticed that memory-consumption by tasks that moved
# files around using FlyteDirectory increased dramatically.  This is documented in
# the flyte-org slack channel:
#
# https://flyte-org.slack.com/archives/CREL4QVAQ/p1683729924011689
#
# The workflow and tasks below allow one to specify a size for file(s)
# and a memory request for the pod.  It can be seen with these tests
# that e.g. writing and uploading a single 2G file on a pod with 2G
# memory causes no issue, but doing so with the many_files option,
# in which 1000 2MB files are uploaded, results in an OOMKilled on the
# task.  Testing using various file size and mem-request size will
# illustrate that the upload of large data requires large amounts of
# memory on flytekit 1.5 and beyond, which was theorized by @Ketan (kumare3)
# to be parallelism in fsspec.  Still, it doesn't feel right that
# uploading 2G of data should require 2G+ of memory.
#
# Resident memory is displayed during the course of the task that
# writes and upload files.  This always reports a low value, even
# after the call to FlyteDirectory(), but the latter continues to
# work in the background and it is theorized by @thomas that the
# implementation is spawning too many file-copy processes, each
# of which is alloc'ing memory which adds up to > mem-request/limit,
# such that the pod is OOMKilled.
#
# Is there a way to control the parallelism of FlyteDirectory to
# avoid this?

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import psutil
import logging
from dataclasses_json import DataClassJsonMixin
from flytekit import Resources, current_context, dynamic, task, workflow, ImageSpec
from flytekit.types.directory import FlyteDirectory

logger = logging.getLogger()

ps_image_spec = ImageSpec(
    base_image="ghcr.io/flyteorg/flytekit:py3.10-1.8.0",
    packages=["psutil", "memray"],
    env={"Debug": "True"},
    apt_packages=["git"],
    registry="ghcr.io/unionai-oss",
)


@dataclass
class Config(DataClassJsonMixin):
    size: int  # total size in GB of file(s) to write and upload
    mem: int  # how much memory the pod should request, in GB
    many_files: bool = False  # write one large file or many smaller files?
    folder: str = ""  # name of the folder to write files to


# ==============================================================================================
# Small utility fns used by task

# Get size of folder using du
def du(path):
    return subprocess.check_output(["du", "-sh", path]).split()[0].decode("utf-8")


# create/clean the folder into which the file(s) will be written for upload
def init_working_dir(path):
    if path and path != '""':
        logger.error(f"Path was detected {path} {type(path)} {len(path)}")
        path = Path(path)
        if path.exists():
            shutil.rmtree(path)
    else:
        logger.error(f"EAttempting to create working directory in {current_context().working_directory}")
        print(f"Attempting to create working directory in {current_context().working_directory}")
        logger.warning(f"Attempting to create working directory in {current_context().working_directory}")
        path = Path(current_context().working_directory) / "test"

    logger.error(f"About to mkdir on {path}")
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


# Get resident (in RAM, not swapped) memory of process
def mem_res():
    resident = psutil.Process().memory_info().rss / (1024 * 1024)
    return f"{resident:.2f}MB"


# Write a single file of size bytes
def write_file(path, size):
    # chunk the size so that we don't have to realize the contents in memory, which
    # would defeat the purpose of this test!
    byte = "0".encode()
    chunks = 1024
    chunksize = size // chunks
    with open(path, "wb") as f:
        for i in range(chunks):
            f.write(byte * chunksize)


# ==============================================================================================
# worker that actually writes one or more files, and initializes a FlyteDirectory with the
# folder, causing those file(s) to be uploaded to s3


def upload_files(folder: str, size: int, many_files: bool) -> FlyteDirectory:
    # size: in GB, total file size to be written, whether one large file or
    # many small files.

    logger.info(
        f"BEGIN upload_files "
        f"{folder=}, size={size}, {many_files=}, resident={mem_res()}"
    )

    # create or clean folder to write to
    folder = init_working_dir(folder)
    logger.info(f"initialized working_dir {folder=}, resident={mem_res()}")

    if many_files:
        # if size is e.g. 2, write 1000 2MB files == 2GB total
        for i in range(4):
            # write files in 4 subfolders to more closely replicate real data examples
            subfolder = f"{folder}/subfolder{i}"
            os.makedirs(subfolder, exist_ok=True)
            for j in range(250):
                write_file(
                    subfolder + f"/big_file_{j}.bin", size * 1024 * 1024
                )  # size in MBs
        # logger.info(
        #     "wrote many files to folder",
        #     size=du(folder),
        #     folder=folder,
        #     resident=mem_res(),
        # )

    else:
        # if size is e.g. 2, write a single 2GB file
        fname = folder + "/big_file.bin"
        write_file(fname, size * 1024 * 1024 * 1024)  # size in GBs
        logger.info(f"wrote single file to folder size={du(folder)}, {folder=}, resident={mem_res()}")

    # FlyteDirectory will cause folder to get uploaded to s3.  This call will return
    # immediately and resident memory will show low memory use.  In the case of 2GB pod-mem request
    # and 2GB worth of files, for a single file the upload will occur without problem, though
    # DataDog memory use shows ~2GB.  For multiple files that add up to 2GB, the task will
    # get OOMKilled *after* the logger statement below, but before the next task runs -- presumably
    # fsspec is consuming too much memory during the upload?

    fd = FlyteDirectory(folder)
    logger.info(f"END upload_files resident={mem_res()}")
    return fd


@task(container_image=ps_image_spec)
def write_files_and_upload(config: Config) -> FlyteDirectory:
    import fsspec.config
    fsspec.config.conf["gather_batch_size"] = 100
    logger.info("BEGIN @task write_files_and_upload", config=config, resident=mem_res())
    fd = upload_files(
        folder=config.folder, size=config.size, many_files=config.many_files
    )

    logger.info(f"upload returned FlyteDirectory fd={fd}, remote_source={fd.remote_source}, resident={mem_res()}")
    logger.info("END @task write_files_and_upload resident=mem_res()")
    # import time; time.sleep(50000)
    return fd


@task(container_image=ps_image_spec)
def download_data_from_flyte_directory(fd: FlyteDirectory) -> str:
    logger.info("BEGIN @task download_data_from_flyte_directory, resident=mem_res()")
    downloaded_path = fd.download()
    # logger.info(
    #     "fd.download() returned", size=du(downloaded_path), remote=fd.remote_source, local=downloaded_path,
    #     resident=mem_res(),
    # )
    logger.info("END @task download_data_from_flyte_directory")
    return downloaded_path


@dynamic(container_image=ps_image_spec)
def flytedirectory_resources_dyn(config: Config) -> str:
    o = {"requests": Resources(mem=f"{config.mem}Gi")}
    logger.info("begin dynamic", overrides=o, config=config)
    fd = write_files_and_upload(config=config).with_overrides(**o)
    return download_data_from_flyte_directory(fd=fd).with_overrides(**o)


@workflow
def flytedirectory_resources(config: Config) -> str:
    return flytedirectory_resources_dyn(config=config)


if __name__ == "__main__":
    res = flytedirectory_resources(config=Config(folder="/Users/ytong/temp/large_files", size=1, many_files=True,
                                                 mem=2))
    print(res)
