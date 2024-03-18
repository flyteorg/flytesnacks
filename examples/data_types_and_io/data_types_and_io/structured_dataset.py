import os
import typing

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from flytekit import FlyteContext, StructuredDatasetType, kwtypes, task, workflow
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


@task
def generate_pandas_df(a: int) -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [a, 22], "Height": [160, 178]})


all_cols = kwtypes(Name=str, Age=int, Height=int)
col = kwtypes(Age=int)


@task
def get_subset_pandas_df(df: Annotated[StructuredDataset, all_cols]) -> Annotated[StructuredDataset, col]:
    df = df.open(pd.DataFrame).all()
    df = pd.concat([df, pd.DataFrame([[30]], columns=["Age"])])
    return StructuredDataset(dataframe=df)


@workflow
def simple_sd_wf(a: int = 19) -> Annotated[StructuredDataset, col]:
    pandas_df = generate_pandas_df(a=a)
    return get_subset_pandas_df(df=pandas_df)


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


class NumpyRenderer:
    def to_html(self, df: np.ndarray) -> str:
        assert isinstance(df, np.ndarray)
        name = ["col" + str(i) for i in range(len(df))]
        table = pa.Table.from_arrays(df, name)
        return pd.DataFrame(table.schema).to_html(index=False)


StructuredDatasetTransformerEngine.register(NumpyEncodingHandler(np.ndarray, None, PARQUET))
StructuredDatasetTransformerEngine.register(NumpyDecodingHandler(np.ndarray, None, PARQUET))
StructuredDatasetTransformerEngine.register_renderer(np.ndarray, NumpyRenderer())


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


if __name__ == "__main__":
    sd = simple_sd_wf()
    print(f"A simple Pandas dataframe workflow: {sd.open(pd.DataFrame).all()}")
    print(f"Using CSV as the serializer: {pandas_to_csv_wf().open(pd.DataFrame).all()}")
    print(f"NumPy encoder and decoder: {numpy_wf().open(np.ndarray).all()}")
