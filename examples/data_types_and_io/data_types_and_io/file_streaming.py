from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
import pandas as pd
import os


@task()
def remove_some_rows(ff: FlyteFile) -> FlyteFile:
    """
    Remove the rows that the value of city is 'Seattle'.
    This is an example with streaming support.
    """
    new_file = FlyteFile.new_remote_file("data_without_seattle.csv")
    with ff.open("r") as r:
        with new_file.open("w") as w:
            df = pd.read_csv(r)
            df = df[df["City"] != "Seattle"]
            df.to_csv(w, index=False)
    return new_file


@task
def process_folder(fd: FlyteDirectory) -> FlyteDirectory:
    out_fd = FlyteDirectory.new_remote("folder-copy")
    for base, x in fd.crawl():
        src = str(os.path.join(base, x))
        out_file = out_fd.new_file(x)
        with FlyteFile(src).open("rb") as f:
            with out_file.open("wb") as o:
                o.write(f.read())
    # The output path will be s3://my-s3-bucket/data/77/<execution-id>-<node-id>-0/folder-copy
    return out_fd


@workflow()
def wf():
    remove_some_rows(ff=FlyteFile("s3://custom-bucket/data.csv"))
    process_folder(fd=FlyteDirectory("s3://my-s3-bucket/folder"))
    return


if __name__ == "__main__":
    print(f"Running wf() {wf()}")
