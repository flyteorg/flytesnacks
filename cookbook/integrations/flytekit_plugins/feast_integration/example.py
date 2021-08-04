from datetime import datetime

import pandas as pd
import feast
from flytekitplugins.feast import (
    DataSourceConfig,
    FeastOfflineRetrieveConfig,
    FeastOfflineRetrieveTask,
    FeastOfflineStoreConfig,
    FeastOfflineStoreTask,
    FeatureViewConfig,
)

from flytekit import kwtypes, task, workflow
from flytekit.types.schema.types import FlyteSchema


feature_view_conf = FeatureViewConfig(
    name="driver_hourly_stats_file",
    features={
        "conv_rate": feast.ValueType.FLOAT,
        "acc_rate": feast.ValueType.FLOAT,
        "avg_daily_trips": feast.ValueType.INT64,
    },
    datasource="file",
    datasource_config=DataSourceConfig(
        event_timestamp_column="datetime",
        created_timestamp_column="created",
        local_file_path="/tmp/test.parquet",
    ),
)
feast_offline_store_conf = FeastOfflineStoreConfig(
    repo_path="feast_integration/feature_repo",
    entities=[("driver_id", feast.ValueType.INT64)],
    feature_view=feature_view_conf,
)

feast_offline_retrieve_conf = FeastOfflineRetrieveConfig(
    entity_val=pd.DataFrame.from_dict(
        {
            "driver_id": [1001, 1002, 1003, 1004],
            "event_timestamp": [
                datetime(2021, 4, 12, 10, 59, 42),
                datetime(2021, 4, 12, 8, 12, 10),
                datetime(2021, 4, 12, 16, 40, 26),
                datetime(2021, 4, 12, 15, 1, 12),
            ],
        }
    ),
    features={feature_view_conf.name: ["conv_rate", "acc_rate", "avg_daily_trips"]},
)

offline_store_task = FeastOfflineStoreTask(
    name="offline_store_schema",
    inputs=kwtypes(dataset=FlyteSchema),
    task_config=feast_offline_store_conf,
)


offline_retrieve_task = FeastOfflineRetrieveTask(
    name="offline_retrieve_schema",
    task_config=feast_offline_retrieve_conf,
)


@task
def get_df(parquet_file: str) -> pd.DataFrame:
    return pd.read_parquet(parquet_file)


@task
def get_df_length(dataframe: pd.DataFrame) -> int:
    return len(dataframe)


@workflow
def feast_offline_workflow() -> int:
    repo_path = offline_store_task(
        dataset=get_df(
            parquet_file="feast_integration/feature_repo/data/driver_stats.parquet"
        )
    )
    dataframe = offline_retrieve_task(repo_path=repo_path)
    return get_df_length(dataframe=dataframe)


if __name__ == "__main__":
    print(feast_offline_workflow())
