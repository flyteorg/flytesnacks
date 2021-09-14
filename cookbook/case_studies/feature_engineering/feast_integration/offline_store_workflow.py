import os
import pandas as pd
from datetime import datetime
from feast import FeatureStore, Entity, FeatureView, FileSource, ValueType, Feature, RepoConfig
from feast.infra.online_stores.sqlite import SqliteOnlineStoreConfig
from feast.infra.offline_stores.file import FileOfflineStoreConfig
from flytekit import task, workflow
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task
from flytekit.types.file.file import FlyteFile
from flytekit.types.schema import FlyteSchema
from datetime import timedelta
# from flyte_file_source import FlyteFileSource

# TODO: find a better way to define these features.
FEAST_FEATURES = [
    "horse_colic_stats:rectal temperature",
    "horse_colic_stats:total protein",
    # "horse_colic_stats:peripheral pulse",
    # "horse_colic_stats:surgical lesion",
    # "horse_colic_stats:abdominal distension",
    # "horse_colic_stats:nasogastric tube",
    # "horse_colic_stats:outcome",
    # "horse_colic_stats:packed cell volume",
    # "horse_colic_stats:nasogastric reflux PH",
]
DATABASE_URI = "https://cdn.discordapp.com/attachments/545481172399030272/861575373783040030/horse_colic.db.zip"

def _build_feature_store(registry: FlyteFile) -> FeatureStore:
    # TODO: comment this
    os.environ["FEAST_S3_ENDPOINT_URL"] = os.environ["FLYTE_AWS_ENDPOINT"]
    os.environ["AWS_ACCESS_KEY_ID"] = os.environ["FLYTE_AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ["FLYTE_AWS_SECRET_ACCESS_KEY"]

    config = RepoConfig(
        registry=registry.remote_source,
        project=f"horsecolic",
        # Notice the use of a custom provider.
        provider="custom_provider.provider.MyCustomProvider",
        offline_store=FileOfflineStoreConfig(),
        online_store=SqliteOnlineStoreConfig(),
    )
    return FeatureStore(config=config)


sql_task = SQLite3Task(
    name="sqlite3.horse_colic",
    query_template="select * from data",
    output_schema_type=FlyteSchema,
    task_config=SQLite3Config(
        uri=DATABASE_URI,
        compressed=True,
    ),
)

@task
def store_offline(registry: FlyteFile, dataframe: FlyteSchema) -> FlyteFile:
    print(f"store_offline remote_source={registry.remote_source}")
    print(f"env vars={os.environ}")
    horse_colic_entity = Entity(name="Hospital Number", value_type=ValueType.STRING)

    horse_colic_feature_view = FeatureView(
        name="horse_colic_stats",
        entities=["Hospital Number"],
        features=[
            Feature(name="rectal temperature", dtype=ValueType.FLOAT),
            Feature(name="total protein", dtype=ValueType.FLOAT),
            # Feature(name="peripheral pulse", dtype=ValueType.FLOAT),
            # Feature(name="surgical lesion", dtype=ValueType.STRING),
            # Feature(name="abdominal distension", dtype=ValueType.FLOAT),
            # Feature(name="nasogastric tube", dtype=ValueType.STRING),
            # Feature(name="outcome", dtype=ValueType.STRING),
            # Feature(name="packed cell volume", dtype=ValueType.FLOAT),
            # Feature(name="nasogastric reflux PH", dtype=ValueType.FLOAT),
        ],
        # Using FlyteFileSource
        # batch_source=FlyteFileSource(
        #     flyte_file=dataframe,
        #     event_timestamp_column="timestamp",
        # ),
        # Using FileSource
        batch_source=FileSource(
            path=str(dataframe.remote_path),
            event_timestamp_column="timestamp",
        ),
        ttl=timedelta(days=1),
    )

    fs = _build_feature_store(registry=registry)

    # Ingest the data into feast
    fs.apply([horse_colic_entity, horse_colic_feature_view])

    return FlyteFile(registry.remote_source)

@task
def load_historical_features(registry: FlyteFile) -> FlyteSchema:
    print(f"load_historical_features remote_source={registry.remote_source}")
    entity_df = pd.DataFrame.from_dict(
        {
            "Hospital Number": [
                "530101",
                "5290409",
                "5291329",
                "530051",
                "529518",
                "530101",
                "529340",
                "5290409",
                "530034",
            ],
            "event_timestamp": [
                datetime(2021, 6, 25, 16, 36, 27),
                datetime(2021, 6, 25, 16, 36, 27),
                datetime(2021, 6, 25, 16, 36, 27),
                datetime(2021, 6, 25, 16, 36, 27),
                datetime(2021, 6, 25, 16, 36, 27),
                datetime(2021, 7, 5, 11, 36, 1),
                datetime(2021, 6, 25, 16, 36, 27),
                datetime(2021, 7, 5, 11, 50, 40),
                datetime(2021, 6, 25, 16, 36, 27),
            ],
        }
    )

    fs = _build_feature_store(registry=registry)
    retrieval_job = fs.get_historical_features(
        entity_df=entity_df,
        features=FEAST_FEATURES,
    )
    return retrieval_job.to_df()


@task
def convert_timestamp_column(dataframe: FlyteSchema, timestamp_column: str) -> FlyteSchema:
    df = dataframe.open().all()
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    return df


@workflow
def load_data_into_offline_store(registry: FlyteFile):
    # Load parquet file from sqlite task
    df = sql_task()
    # Need to convert timestamp column in the underlying dataframe, otherwise its type is written as
    # string. There is probably a better way of doing this conversion.
    converted_df = convert_timestamp_column(dataframe=df, timestamp_column="timestamp")

    store_offline(registry=registry, dataframe=converted_df)

    feature_data = load_historical_features(registry=registry)

if __name__ == '__main__':
    print(f"{load_data_into_offline_store(registry='s3://feast-integration/registry-2.db')}")
    # print(f"{load_data_into_offline_store(registry_uri='./registry.db')}")
