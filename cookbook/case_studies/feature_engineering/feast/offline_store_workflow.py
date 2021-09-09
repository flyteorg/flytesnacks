from feast import FeatureStore, Entity, FeatureView, FileSource, ValueType, Feature, RepoConfig, repo_config
from flytekit import task, workflow
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task
from flytekit.types.schema import FlyteSchema
from datetime import timedelta

DATABASE_URI = "https://cdn.discordapp.com/attachments/545481172399030272/861575373783040030/horse_colic.db.zip"


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
def store_offline(dataframe: FlyteSchema) -> (str, str):
    # Build RepoConfig
    config = RepoConfig(
        registry="s3://feast-integration/registry.db",
        project=f"horse-colic",
        provider="local",
        # online_store=DatastoreOnlineStoreConfig(namespace="integration_test"),
    )
    fs = FeatureStore(config=config)
    horse_colic_entity = Entity(name="Hospital Number", value_type=ValueType.STRING)

    horse_colic_feature_view = FeatureView(
        name="horse_colic_stats",
        entities=["Hospital Number"],
        features=[
            Feature(name="rectal temperature", dtype=ValueType.FLOAT),
            Feature(name="total protein", dtype=ValueType.FLOAT),
            Feature(name="peripheral pulse", dtype=ValueType.FLOAT),
            Feature(name="surgical lesion", dtype=ValueType.STRING),
            Feature(name="abdominal distension", dtype=ValueType.FLOAT),
            Feature(name="nasogastric tube", dtype=ValueType.STRING),
            Feature(name="outcome", dtype=ValueType.STRING),
            Feature(name="packed cell volume", dtype=ValueType.FLOAT),
            Feature(name="nasogastric reflux PH", dtype=ValueType.FLOAT),
        ],
        input=FileSource(
            path=str(dataframe.remote_path),
            event_timestamp_column="timestamp",
        ),
        ttl=timedelta(days=1),
    )

    fs.apply([horse_colic_entity, horse_colic_feature_view])
    return repo_path, horse_colic_feature_view.name

@workflow
def load_data_into_offline_store(feast_repo_path: str):
    # Load parquet file from sqlite task
    df = sql_task()
    a, b = store_offline(dataframe=df)

if __name__ == '__main__':
    print(f"{load_data_into_offline_store(feast_repo_path='some-path')}")
