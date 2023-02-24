import fsspec
import os
from fsspec.utils import get_protocol
from flytekit import task, workflow, current_context, FlyteContextManager
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from flytekit.core.data_persistence import FileAccessProvider
from flytekit.configuration import Config

import io

def stream_opener(path: str, mode: int):
    """
    Uses fsspec to open the file that is passed and returns a stream for the same.
    Usage:
        ff: FlyteFile
        with open(ff.remote_path, "rb", opener=stream_opener) as f:
            b = f.read()
    """
    protocol = get_protocol(path)
    print(f"Mode {mode}, {type(mode)}")
    fs: fsspec.AbstractFileSystem = fsspec.filesystem(protocol)
    x = fs.open(path, "rb")
    return x.f.fileno()
        # print(ff.read())
        # return ff.f.fileno()
    # with fs.open(path, "rb") as ff:
    #     return ff.f.fileno()
    # return x.fileno()
    # return x



def new_remote_path() -> str:
    ctx = FlyteContextManager.current_context()
    return ctx.file_access.get_random_remote_path()


@task
def copy_file(ff: FlyteFile) -> FlyteFile:
    # We need a place to write a new file
    # ideally new_file = current_ctx().new_remote_file_path
    out_file = new_remote_path()
    print(f"New remote path is: {out_file}")
    with open(ff, "rb", opener=stream_opener, buffering=1024) as r:
        print(r.read())
        # with open(out_file, "wb", opener=stream_opener) as w:
        #     w.write(r.read())
    return FlyteFile(path="", remote_path=out_file)


@task
def process_folder(fd: FlyteDirectory):
    for f in fsspec.open_files(fd.remote_directory):
        b = f.read()
        print(f"Len {f.name} -> {len(b)}")


@workflow
def wf(fd: FlyteDirectory, ff: FlyteFile):
    copy_file(ff=ff)
    process_folder(fd=fd)


if __name__ == "__main__":
    numbers1 = [1, 2, 3]
    numbers2 = [4, 5, 6]

    result = map(lambda x, y, z: x + y + z, numbers1, numbers2, [4, 1])
    print(list(result))

    # ctx = FlyteContextManager.current_context()
    # new_f = FileAccessProvider(
    #     local_sandbox_dir=ctx.file_access.local_sandbox_dir,
    #     raw_output_prefix="s3://my-s3-bucket/streamed",
    #     data_config=Config.for_sandbox().data_config,
    # )
    # with FlyteContextManager.with_context(ctx.new_builder().with_file_access(new_f)) as ctx:
    #     print(ctx)
    #     print(f"Sample: {ctx.file_access.get_random_remote_path()}")
    #     copy_file(ff=FlyteFile(path="/tmp/file_a", remote_path=False))
