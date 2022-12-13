from io import StringIO

import boto3
import pandas as pd
from flytekit import FlyteContext, task, workflow, kwtypes
from flytekit.extras.persistence.s3_awscli import S3Persistence
from flytekit.models import literals
from flytekit.models.literals import StructuredDatasetMetadata
from flytekit.types.structured.structured_dataset import (
    PARQUET,
    StructuredDatasetDecoder,
    StructuredDatasetTransformerEngine,
)
from typing_extensions import Annotated


class ExperimentalNaiveS3SelectDecoder(StructuredDatasetDecoder):
    def __init__(self):
        super().__init__(pd.DataFrame, "s3", PARQUET)

    def decode(
        self,
        ctx: FlyteContext,
        flyte_value: literals.StructuredDataset,
        current_task_metadata: StructuredDatasetMetadata,
    ) -> pd.DataFrame:
        if current_task_metadata.structured_dataset_type and current_task_metadata.structured_dataset_type.columns:
            columns = [c.name for c in current_task_metadata.structured_dataset_type.columns]
            sql_cols = ",".join(columns)
        else:
            sql_cols = "*"

        # S3 select only works on individual files, and the default flytekit pandas encoder will write the file with
        # a filename of 00000
        s3_file = flyte_value.uri + "/00000"
        sql = f"select {sql_cols} from s3object"

        bucket, prefix = S3Persistence._split_s3_path_to_bucket_and_key(s3_file)  # noqa
        print(f"Selecting from {bucket}, {prefix}, original uri {flyte_value.uri} with query {sql}")
        s3 = boto3.client("s3")
        r = s3.select_object_content(
            Bucket=bucket,
            Key=prefix,
            ExpressionType="SQL",
            Expression=sql,
            InputSerialization={"Parquet": {}},
            OutputSerialization={"CSV": {}},
        )

        lines = []
        for event in r['Payload']:
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8')
                if not str(records) == "":
                    lines.append(records)
        lines = "\n".join(lines)
        df = pd.read_csv(StringIO(lines))
        print(f"Selected df")
        return df


StructuredDatasetTransformerEngine.register(ExperimentalNaiveS3SelectDecoder(), override=True)


@task
def make_df() -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph", "Harry"], "Age": [20, 22, 20]})


@task
def use_df(a: Annotated[pd.DataFrame, kwtypes(Name=str)]) -> str:
    msg = f"This is the subset dataframe\n{a}"
    print(msg)
    return msg


@workflow
def ex():
    df = make_df()
    use_df(a=df)


if __name__ == "__main__":
    ex()
