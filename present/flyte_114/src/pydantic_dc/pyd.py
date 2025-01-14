from enum import Enum
import pandas as pd
import os

import flytekit as fl
import tempfile

from pydantic import BaseModel, Field
from typing import Dict, List
from random import choice
from string import ascii_letters
from flytekit.types.structured import StructuredDataset
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
import aiohttp

aiohttp.ClientSession

class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Leaf(BaseModel):
    list_ints: List[int] = Field(default_factory=lambda: [0, 1, 2, -1, -2])
    list_files: List[FlyteFile] = Field(
        default_factory=lambda: [FlyteFile("s3://my-s3-bucket/s3_flyte_dir/example.txt")]
    )
    dict_files: Dict[int, FlyteFile] = Field(
        default_factory=lambda: {
            0: FlyteFile("s3://my-s3-bucket/s3_flyte_dir/example.txt"),
            1: FlyteFile("s3://my-s3-bucket/s3_flyte_dir/example.txt"),
            -1: FlyteFile("s3://my-s3-bucket/s3_flyte_dir/example.txt"),
        }
    )
    enum_status: Status = Status.PENDING
    sd: StructuredDataset = Field(
        default_factory=lambda: StructuredDataset(
            uri="s3://my-s3-bucket/s3_flyte_dir/df.parquet", file_format="parquet"
        )
    )


class Parent(BaseModel):
    o: FlyteDirectory = Field(default_factory=lambda: FlyteDirectory("s3://my-s3-bucket/s3_flyte_dir"))
    leaf_model: Leaf = Field(default_factory=lambda: Leaf())


@fl.task
def create_file() -> FlyteFile:
    with open("example.txt", "w") as f:
        f.write("Default content -- ")
        f.write("".join(choice(ascii_letters) for _ in range(20)))
    return FlyteFile("example.txt")


@fl.task
def create_dir() -> FlyteDirectory:
    wk_dir = fl.current_context().working_directory
    fl.current_context().logging.info(f"Working directory: {wk_dir}")
    tmp = tempfile.mkdtemp(dir=wk_dir)
    with open(os.path.join(tmp, "example_1.txt"), "w") as f:
        f.write("Default content 1")
    with open(os.path.join(tmp, "example_2.txt"), "w") as f:
        f.write("Default content 2")
    return FlyteDirectory(tmp)


@fl.task
def create_sd() -> StructuredDataset:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    return StructuredDataset(dataframe=df)


@fl.task
def create_parent(file_1: FlyteFile, file_2: FlyteFile, folder: FlyteDirectory, sd: StructuredDataset) -> Parent:
    leaf = Leaf(
        list_ints=[1, 2, 2, 1],
        list_files=[file_1, file_2],
        sd=sd,
    )

    p = Parent(
        o=folder,
        leaf_model=leaf,
    )

    return p


@fl.task
def leaf_print(leaf: Leaf):
    assert isinstance(leaf, Leaf)

    # Show all the fields of Leaf
    print(f"Leaf: {leaf}")

    print("\n\n")
    print("====== File Contents ======")
    for i, f in enumerate(leaf.list_files):
        print(f"File {i}:: Local file: {f.path} Remote location: {f.remote_source}")
        with open(f, "r") as fh:
            print(fh.read())
        print("<<EOF")

    print("\n\n")
    print("====== Structured Dataset ======")
    print(f"Structured Dataset: {leaf.sd.uri}")
    df = leaf.sd.open(pd.DataFrame).all()
    print(df)


@fl.workflow
def wf():
    get_file_1 = create_file()
    get_file_2 = create_file()
    get_folder = create_dir()
    get_sd = create_sd()
    parent = create_parent(file_1=get_file_1, file_2=get_file_2, folder=get_folder, sd=get_sd)
    leaf_print(leaf=parent.leaf_model)
