import os
import typing
from dataclasses import dataclass

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from flytekit import FlyteContext, ImageSpec, StructuredDatasetType, kwtypes, task, workflow
from flytekit.models import literals
from flytekit.models.literals import StructuredDatasetMetadata
from flytekit.types.structured.structured_dataset import (
    PARQUET,
    StructuredDataset,
    StructuredDatasetDecoder,
    StructuredDatasetEncoder,
    StructuredDatasetTransformerEngine,
)
from typing_extensions import Annotated


# Define a task that returns a Pandas DataFrame.
# Flytekit will detect the Pandas dataframe return signature and
# convert the interface for the task to the StructuredDatased type
@task
def generate_pandas_df(a: int) -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [a, 22], "Height": [160, 178]})


# Initialize column types you want to extract from the `StructuredDataset`
all_cols = kwtypes(Name=str, Age=int, Height=int)
col = kwtypes(Age=int)


# Define a task that opens a structured dataset by calling `all()`.
# When you invoke `all()` with `pandas.DataFrame`, the Flyte engine downloads
# the parquet file on S3, and deserializes it to `pandas.DataFrame`.
# Keep in mind that you can invoke ``open()`` with any dataframe type
# that's supported or added to structured dataset.
# For instance, you can use ``pa.Table`` to convert
# the Pandas DataFrame to a PyArrow table.
@task
def get_subset_pandas_df(df: Annotated[StructuredDataset, all_cols]) -> Annotated[StructuredDataset, col]:
    df = df.open(pd.DataFrame).all()
    df = pd.concat([df, pd.DataFrame([[30]], columns=["Age"])])
    return StructuredDataset(dataframe=df)


@workflow
def simple_sd_wf(a: int = 19) -> Annotated[StructuredDataset, col]:
    pandas_df = generate_pandas_df(a=a)
    return get_subset_pandas_df(df=pandas_df)


# You can use a custom serialization format to serialize your dataframes.
# Here's how you can register the Pandas to CSV handler, which is already available,
# and enable the CSV serialization by annotating the structured dataset with the CSV format:
from flytekit.types.structured import register_csv_handlers
from flytekit.types.structured.structured_dataset import CSV

register_csv_handlers()


@task
def pandas_to_csv(df: pd.DataFrame) -> Annotated[StructuredDataset, CSV]:
    return StructuredDataset(dataframe=df)


@workflow
def pandas_to_csv_wf() -> Annotated[StructuredDataset, CSV]:
    pandas_df = generate_pandas_df(a=19)
    return pandas_to_csv(df=pandas_df)


# Extend `StructuredDatasetEncoder` and implement the `encode` function.
# The `encode` function converts NumPy array to an intermediate format
# (parquet file format in this case).
class NumpyEncodingHandler(StructuredDatasetEncoder):
    def encode(
        self,
        ctx: FlyteContext,
        structured_dataset: StructuredDataset,
        structured_dataset_type: StructuredDatasetType,
    ) -> literals.StructuredDataset:
        df = typing.cast(np.ndarray, structured_dataset.dataframe)
        name = ["col" + str(i) for i in range(len(df))]
        table = pa.Table.from_arrays(df, name)
        path = ctx.file_access.get_random_remote_directory()
        local_dir = ctx.file_access.get_random_local_directory()
        local_path = os.path.join(local_dir, f"{0:05}")
        pq.write_table(table, local_path)
        ctx.file_access.upload_directory(local_dir, path)
        return literals.StructuredDataset(
            uri=path,
            metadata=StructuredDatasetMetadata(structured_dataset_type=StructuredDatasetType(format=PARQUET)),
        )


# Extend `StructuredDatasetDecoder` and implement the `StructuredDatasetDecoder.decode` function.
# The `StructuredDatasetDecoder.decode` function converts the parquet file to a `numpy.ndarray`
class NumpyDecodingHandler(StructuredDatasetDecoder):
    def decode(
        self,
        ctx: FlyteContext,
        flyte_value: literals.StructuredDataset,
        current_task_metadata: StructuredDatasetMetadata,
    ) -> np.ndarray:
        local_dir = ctx.file_access.get_random_local_directory()
        ctx.file_access.get_data(flyte_value.uri, local_dir, is_multipart=True)
        table = pq.read_table(local_dir)
        return table.to_pandas().to_numpy()


# Create a default renderer for numpy array, then Flytekit will use this renderer to
# display schema of NumPy array on the Flyte Deck
class NumpyRenderer:
    def to_html(self, df: np.ndarray) -> str:
        assert isinstance(df, np.ndarray)
        name = ["col" + str(i) for i in range(len(df))]
        table = pa.Table.from_arrays(df, name)
        return pd.DataFrame(table.schema).to_html(index=False)


# In the end, register the encoder, decoder and renderer with the `StructuredDatasetTransformerEngine`.
# Specify the Python type you want to register this encoder with (`np.ndarray`),
# the storage engine to register this against (if not specified, it is assumed to work for all the storage backends),
# and the byte format, which in this case is `PARQUET`.
StructuredDatasetTransformerEngine.register(NumpyEncodingHandler(np.ndarray, None, PARQUET))
StructuredDatasetTransformerEngine.register(NumpyDecodingHandler(np.ndarray, None, PARQUET))
StructuredDatasetTransformerEngine.register_renderer(np.ndarray, NumpyRenderer())


# You can now use `numpy.ndarray` to deserialize the parquet file to NumPy
# and serialize a task's output (NumPy array) to a parquet file.
@task
def generate_pd_df_with_str() -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph"]})


@task
def to_numpy(sd: StructuredDataset) -> Annotated[StructuredDataset, None, PARQUET]:
    numpy_array = sd.open(np.ndarray).all()
    return StructuredDataset(dataframe=numpy_array)


@workflow
def numpy_wf() -> Annotated[StructuredDataset, None, PARQUET]:
    return to_numpy(sd=generate_pd_df_with_str())


# Run the code locally
if __name__ == "__main__":
    sd = simple_sd_wf()
    print(f"A simple Pandas dataframe workflow: {sd.open(pd.DataFrame).all()}")
    print(f"Using CSV as the serializer: {pandas_to_csv_wf().open(pd.DataFrame).all()}")
    print(f"NumPy encoder and decoder: {numpy_wf().open(np.ndarray).all()}")

data = [
    {
        "company": "XYZ pvt ltd",
        "location": "London",
        "info": {"president": "Rakesh Kapoor", "contacts": {"email": "contact@xyz.com", "tel": "9876543210"}},
    },
    {
        "company": "ABC pvt ltd",
        "location": "USA",
        "info": {"president": "Kapoor Rakesh", "contacts": {"email": "contact@abc.com", "tel": "0123456789"}},
    },
]


@dataclass
class ContactsField:
    email: str
    tel: str


@dataclass
class InfoField:
    president: str
    contacts: ContactsField


@dataclass
class CompanyField:
    location: str
    info: InfoField
    company: str


MyArgDataset = Annotated[StructuredDataset, kwtypes(company=str)]
MyTopDataClassDataset = Annotated[StructuredDataset, CompanyField]
MyTopDictDataset = Annotated[StructuredDataset, {"company": str, "location": str}]

MyDictDataset = Annotated[StructuredDataset, kwtypes(info={"contacts": {"tel": str}})]
MyDictListDataset = Annotated[StructuredDataset, kwtypes(info={"contacts": {"tel": str, "email": str}})]
MySecondDataClassDataset = Annotated[StructuredDataset, kwtypes(info=InfoField)]
MyNestedDataClassDataset = Annotated[StructuredDataset, kwtypes(info=kwtypes(contacts=ContactsField))]

image = ImageSpec(packages=["pandas", "tabulate"], registry="ghcr.io/flyteorg")


@task(container_image=image)
def create_parquet_file() -> StructuredDataset:
    from tabulate import tabulate
    df = pd.json_normalize(data, max_level=0)
    print("original dataframe: \n", tabulate(df, headers="keys", tablefmt="psql"))

    return StructuredDataset(dataframe=df)


@task(container_image=image)
def print_table_by_arg(sd: MyArgDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MyArgDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@task(container_image=image)
def print_table_by_dict(sd: MyDictDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MyDictDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@task(container_image=image)
def print_table_by_list_dict(sd: MyDictListDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MyDictListDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@task(container_image=image)
def print_table_by_top_dataclass(sd: MyTopDataClassDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MyTopDataClassDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@task(container_image=image)
def print_table_by_top_dict(sd: MyTopDictDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MyTopDictDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@task(container_image=image)
def print_table_by_second_dataclass(sd: MySecondDataClassDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MySecondDataClassDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@task(container_image=image)
def print_table_by_nested_dataclass(sd: MyNestedDataClassDataset) -> pd.DataFrame:
    from tabulate import tabulate
    t = sd.open(pd.DataFrame).all()
    print("MyNestedDataClassDataset dataframe: \n", tabulate(t, headers="keys", tablefmt="psql"))
    return t


@workflow
def contacts_wf():
    sd = create_parquet_file()
    print_table_by_arg(sd=sd)
    print_table_by_dict(sd=sd)
    print_table_by_list_dict(sd=sd)
    print_table_by_top_dataclass(sd=sd)
    print_table_by_top_dict(sd=sd)
    print_table_by_second_dataclass(sd=sd)
    print_table_by_nested_dataclass(sd=sd)
