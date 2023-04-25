import typing
import boto3
import re
import os
from pathlib import Path

import pandas as pd
from pyspark.sql import DataFrame as sparkDF
import tempfile


c = boto3.client("s3", endpoint_url="http://localhost:30002")


def upload_file_to_s3(file_path: str):
    s3_client = boto3.client("s3")
    s3_client.upload_file(file_path, "data-bucket-one", "hello-remote.txt")


def upload_dataframe(df: pd.DataFrame):
    fd, path = tempfile.mkstemp()
    df.to_parquet(path)
    upload_file_to_s3(path)


def download_files(s3_client, bucket_name, prefix, local_path):
    local_path = Path(local_path)
    local_path.mkdir(parents=True, exist_ok=True)
    ll = s3_client.list_objects(Bucket=bucket_name,
        Prefix=prefix,
    )

    prefix_parts = [x for x in prefix.split("/") if x]

    all_keys = [x["Key"] for x in ll["Contents"]]
    for k in all_keys:
        folders = k.split("/")
        new_file = local_path.joinpath(os.path.join(*folders[len(prefix_parts):]))
        new_file.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {bucket_name}/{k} to {str(new_file)}")
        s3_client.download_file(bucket_name, k, str(new_file))


def analyze_spark(sdf: sparkDF):
    df = sdf.toPandas()
    ...


def analyze_with_spark(df: pd.DataFrame):
    from pyspark.sql import SparkSession
    session = SparkSession.builder \
        .master("local[1]") \
        .appName("pydatademo") \
        .getOrCreate()
    sdf = session.createDataFrame(df)
    ...


def download_file_from_s3(s3_path):
    # Extract the bucket and key from the S3 path
    match = re.match(r's3://([^/]+)/(.+)', s3_path)
    if not match:
        raise ValueError(f"Invalid S3 path: {s3_path}")

    bucket, key = match.groups()

    # Create a boto3 client for S3
    s3_client = boto3.client('s3')

    # Download the file
    tmp = tempfile.mktemp()
    s3_client.download_file(bucket, key, tmp)
    return tmp


def to_html(self, html_elements: typing.List[str]) -> str:
    grid_items = "\n".join([f'<div class="grid-item">{element}</div>' for element in html_elements])
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .grid-container {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                grid-gap: 10px;
                padding: 10px;
            }}
            .grid-item {{
                padding: 10px;
                background-color: #f1f1f1;
                border: 1px solid #ccc;
                border-radius: 5px;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: auto;
                max-height: 300px; /* Adjust this value to set the maximum height of the grid item */
            }}
            .grid-item img {{
                display: block;
                max-width: 100%;
                max-height: 100%;
            }}
        </style>
    </head>
    <body>
        <div class="grid-container">
            {grid_items}
        </div>
    </body>
    </html>
    '''
