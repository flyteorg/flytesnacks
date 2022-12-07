import typing
import pandas as pd
import os

from flytekit import FlyteContext, task, workflow
from flytekit.models import literals
from flytekit.models.literals import StructuredDatasetMetadata
from flytekit.types.structured.structured_dataset import (
    PARQUET,
    StructuredDataset,
    StructuredDatasetDecoder,
    StructuredDatasetEncoder,
    StructuredDatasetTransformerEngine,
    StructuredDatasetType,
)


class DummyPandasToParquetEncodingHandler(StructuredDatasetEncoder):
    def __init__(self):
        super().__init__(pd.DataFrame, "/", PARQUET)

    def encode(
        self,
        ctx: FlyteContext,
        structured_dataset: StructuredDataset,
        structured_dataset_type: StructuredDatasetType,
    ) -> literals.StructuredDataset:

        path = typing.cast(str, structured_dataset.uri) or ctx.file_access.get_random_remote_directory()
        df = typing.cast(pd.DataFrame, structured_dataset.dataframe)
        local_dir = ctx.file_access.get_random_local_directory()
        df.to_parquet(local_dir, coerce_timestamps="us", allow_truncated_timestamps=False, partition_cols=["Age"])
        print(f"Writing dataframe to folder {local_dir}")
        ctx.file_access.upload_directory(local_dir, path)
        structured_dataset_type.format = PARQUET
        return literals.StructuredDataset(uri=path, metadata=StructuredDatasetMetadata(structured_dataset_type))


class DummyParquetToPandasDecodingHandler(StructuredDatasetDecoder):
    def __init__(self):
        super().__init__(pd.DataFrame, "/", PARQUET)

    def decode(
        self,
        ctx: FlyteContext,
        flyte_value: literals.StructuredDataset,
        current_task_metadata: StructuredDatasetMetadata,
    ) -> typing.Generator[pd.DataFrame, None, None]:
        local_dir = ctx.file_access.get_random_local_directory()
        if current_task_metadata.structured_dataset_type and current_task_metadata.structured_dataset_type.columns:
            columns = [c.name for c in current_task_metadata.structured_dataset_type.columns]

        # dummy example, can rely on os.listdir because we know the "remote" here is just a local file
        partitioned_folders = os.listdir(flyte_value.uri)
        for p in partitioned_folders:
            # for each partition, download and then construct a dataframe
            subfolder_src = os.path.join(flyte_value.uri, p)
            subfolder_dest = os.path.join(local_dir, p)
            print(f"Downloading {subfolder_src} to {subfolder_dest}")
            ctx.file_access.get_data(subfolder_src, subfolder_dest, is_multipart=True)
            yield pd.read_parquet(local_dir)


StructuredDatasetTransformerEngine.register(DummyPandasToParquetEncodingHandler(), override=True, default_for_type=True)
StructuredDatasetTransformerEngine.register(DummyParquetToPandasDecodingHandler(), override=True, default_for_type=True)


@task
def make_df() -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph", "Harry"], "Age": [20, 22, 20]})


@task
def use_df(a: StructuredDataset):
    for dd in a.open(pd.DataFrame).iter():
        print(f"This is a partial dataframe")
        print(dd)


@workflow
def ex():
    df = make_df()
    use_df(a=df)


if __name__ == "__main__":
    ex()
