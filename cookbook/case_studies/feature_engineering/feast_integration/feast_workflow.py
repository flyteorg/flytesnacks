"""
Flyte Pipeline With Feast
-------------------------

This workflow makes use of the feature engineering tasks defined in the other file. We'll build an end-to-end Flyte
pipeline utilizing "Feast". Here is the step-by-step process:

* Fetch the SQLite3 data as a Pandas DataFrame
* Perform mean-median-imputation
* Build a feature store
* Store the updated features in an offline store
* Retrieve the features from an offline store
* Perform univariate-feature-selection
* Train a Naive Bayes model
* Load features into an online store
* Fetch one feature vector for inference
* Generate prediction
"""

import logging
import random
import os
import numpy as np
import flytekit

# %%
# Let's import the libraries.
from datetime import datetime, timedelta
import boto3
import joblib
import pandas as pd
from feast import Entity, FeatureStore, FeatureView, FileSource, Field

# from feast_dataobjects import FeatureStore, FeatureStoreConfig  # noqa : F811
from flytekit import Resources, TaskMetadata, task, workflow, reference_task
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task
from flytekit.types.file import JoblibSerializedFile
from flytekit.types.structured import StructuredDataset
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from feast.types import Float64, String
from flytekit import FlyteContext
from feast.infra.offline_stores.file import FileOfflineStoreConfig
from feast.infra.online_stores.sqlite import SqliteOnlineStoreConfig
from feast.repo_config import RepoConfig
from flytekit.types.file import FlyteFile

logger = logging.getLogger(__file__)

S3_BUCKET = "feast-integration"
REGISTRY_PATH = "registry.db"
ONLINE_STORE_PATH = "online.db"

try:
    from feature_eng_tasks import mean_median_imputer, univariate_selection
except ImportError:
    from .feature_eng_tasks import mean_median_imputer, univariate_selection

if os.getenv("SANDBOX") != "":
    ENDPOINT = "http://minio.flyte:9000"
else:
    # local execution
    ENDPOINT = "http://localhost:30084"

os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"
os.environ["FEAST_S3_ENDPOINT_URL"] = ENDPOINT


# %%
# We define the necessary data holders.

# TODO: find a better way to define these features.
FEAST_FEATURES = [
    "horse_colic_stats:rectal temperature",
    "horse_colic_stats:total protein",
    "horse_colic_stats:peripheral pulse",
    "horse_colic_stats:surgical lesion",
    "horse_colic_stats:abdominal distension",
    "horse_colic_stats:nasogastric tube",
    "horse_colic_stats:outcome",
    "horse_colic_stats:packed cell volume",
    "horse_colic_stats:nasogastric reflux PH",
]
DATABASE_URI = "https://cdn.discordapp.com/attachments/545481172399030272/861575373783040030/horse_colic.db.zip"
DATA_CLASS = "surgical lesion"


# %%
# This task exists just for the sandbox case, as Feast needs an explicit S3 bucket and path.
# We will create it using an S3 client. This unfortunately makes the workflow less portable.
@task
def create_bucket(bucket_name: str) -> RepoConfig:
    client = boto3.client(
        "s3",
        aws_access_key_id="minio",
        aws_secret_access_key="miniostorage",
        use_ssl=False,
        endpoint_url=ENDPOINT,
    )

    try:
        client.create_bucket(Bucket=bucket_name)
    except client.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"Bucket {bucket_name} has already been created by you.")
        pass

    return RepoConfig(
        registry=f"s3://{S3_BUCKET}/{REGISTRY_PATH}",
        project="horsecolic",
        provider="aws",
        offline_store=FileOfflineStoreConfig(),
        online_store=SqliteOnlineStoreConfig(path=ONLINE_STORE_PATH),
    )


# %%
# This is the first task and represents the data source. This can be any task, that fetches data, generates, modifies
# data ready for feature ingestion. These can also be arbitrary feature engineering tasks like data imputation, univariate
# selection, etc.
load_horse_colic_sql = SQLite3Task(
    name="sqlite3.load_horse_colic",
    query_template="select * from data",
    output_schema_type=pd.DataFrame,
    task_config=SQLite3Config(
        uri=DATABASE_URI,
        compressed=True,
    ),
    metadata=TaskMetadata(
        cache=True,
        cache_version="1.0",
    ),
)


# %%
# We define two tasks, namely ``store_offline`` and ``load_historical_features`` to store and retrieve the historial
# features.
#
# .. list-table:: Decoding the ``Feast`` Nomenclature
#    :widths: 25 25
#
#    * - ``FeatureStore``
#      - A FeatureStore object is used to define, create, and retrieve features.
#    * - ``Entity``
#      - Represents a collection of entities and associated metadata. It's usually the primary key of your data.
#    * - ``FeatureView``
#      - A FeatureView defines a logical grouping of serve-able features.
#    * - ``FileSource``
#      - File data sources allow for the retrieval of historical feature values from files on disk for building training datasets, as well as for materializing features into an online store.
#    * - ``apply()``
#      - Register objects to metadata store and update related infrastructure.
#    * - ``get_historical_features()``
#      - Enrich an entity dataframe with historical feature values for either training or batch scoring.
#
# .. note::
#
#     The returned feature store is the same mutated feature store, so be careful! This is not really immutable and
#     hence serialization of the feature store is required because FEAST registries are single files and
#     Flyte workflows can be highly concurrent.
@task(limits=Resources(mem="400Mi"))
def store_offline(repo_config: RepoConfig, dataframe: StructuredDataset) -> FlyteFile:
    horse_colic_entity = Entity(name="Hospital Number")

    ctx = flytekit.current_context()
    data_dir = os.path.join(ctx.working_directory, "parquet-data")
    os.makedirs(data_dir, exist_ok=True)

    FlyteContext.current_context().file_access.get_data(
        dataframe._literal_sd.uri + "/00000",
        dataframe._literal_sd.uri + ".parquet",
    )

    horse_colic_feature_view = FeatureView(
        name="horse_colic_stats",
        entities=[horse_colic_entity],
        schema=[
            Field(name="rectal temperature", dtype=Float64),
            Field(name="total protein", dtype=Float64),
            Field(name="peripheral pulse", dtype=Float64),
            Field(name="surgical lesion", dtype=String),
            Field(name="abdominal distension", dtype=Float64),
            Field(name="nasogastric tube", dtype=String),
            Field(name="outcome", dtype=String),
            Field(name="packed cell volume", dtype=Float64),
            Field(name="nasogastric reflux PH", dtype=Float64),
        ],
        source=FileSource(
            path=dataframe._literal_sd.uri + ".parquet",
            timestamp_field="timestamp",
            s3_endpoint_override="http://minio.flyte:9000",
        ),
        ttl=timedelta(days=1),
    )

    # Ingest the data into feast
    FeatureStore(config=repo_config).apply(
        [horse_colic_entity, horse_colic_feature_view]
    )

    return FlyteFile(path=ONLINE_STORE_PATH)


@task(limits=Resources(mem="400Mi"))
def load_historical_features(repo_config: RepoConfig) -> pd.DataFrame:
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

    historical_features = (
        FeatureStore(config=repo_config)
        .get_historical_features(entity_df=entity_df, features=FEAST_FEATURES)
        .to_df()
    )  # noqa

    return historical_features


# %%
# Next, we train a naive bayes model using the data from the feature store.
@task
def train_model(dataset: pd.DataFrame, data_class: str) -> JoblibSerializedFile:
    x_train, _, y_train, _ = train_test_split(
        dataset[dataset.columns[~dataset.columns.isin([data_class])]],
        dataset[data_class],
        test_size=0.33,
        random_state=42,
    )
    model = GaussianNB()
    model.fit(x_train, y_train)
    model.feature_names = list(x_train.columns.values)
    fname = "/tmp/model.joblib.dat"
    joblib.dump(model, fname)
    return fname


# %%
# To perform inferencing, we define two tasks: ``store_online`` and ``retrieve_online``.
#
# .. list-table:: Decoding the ``Feast`` Nomenclature
#    :widths: 25 25
#
#    * - ``materialize()``
#      - Materialize data from the offline store into the online store.
#    * - ``get_online_features()``
#      - Retrieves the latest online feature data.
#
# .. note::
#
#   One key difference between an online and offline store is that only the latest feature values are stored per entity
#   key in an online store, unlike an offline store where all feature values are stored.
#   Our dataset has two such entries with the same ``Hospital Number`` but different time stamps.
#   Only data point with the latest timestamp will be stored in the online store.
@task(limits=Resources(mem="400Mi"))
def store_online(repo_config: RepoConfig, online_store_file: FlyteFile) -> FlyteFile:
    FlyteContext.current_context().file_access.get_data(
        online_store_file.download(), ONLINE_STORE_PATH
    )

    FeatureStore(config=repo_config).materialize(
        start_date=datetime.utcnow() - timedelta(days=2000),
        end_date=datetime.utcnow() - timedelta(minutes=10),
    )

    return FlyteFile(path=ONLINE_STORE_PATH)


# %%
# We define a task to test our model using the inference point fetched earlier.
@task
def predict(model_ser: JoblibSerializedFile, features: dict) -> np.ndarray:
    # Load model
    model = joblib.load(model_ser)
    f_names = model.feature_names

    test_list = []
    for each_name in f_names:
        test_list.append(features[each_name][0])

    if all(test_list):
        prediction = model.predict([[float(x) for x in test_list]])
    else:
        prediction = ["The requested data is not found in the online feature store"]
    return prediction


# %%
# Next, we need to convert timestamp column in the underlying dataframe, otherwise its type is written as string.
@task(cache=True, cache_version="2.0")
def convert_timestamp_column(
    dataframe: pd.DataFrame, timestamp_column: str
) -> pd.DataFrame:
    dataframe[timestamp_column] = pd.to_datetime(dataframe[timestamp_column])
    return dataframe


# # %%
# # The ``build_FEATURE_STORE`` task is a medium to access Feast methods by building a feature store.
# def build_FEATURE_STORE(
#     s3_bucket: str, registry_path: str, online_store_path: str
# ) -> FeatureStore:


# %%
# A sample method that randomly selects one datapoint from the input dataset to run predictions on.
#
# .. note::
#
#    Note this is not ideal and can be just embedded in the predict method. But, for introspection and demo, we are
#    splitting it up.
#
@task
def retrieve_online(
    repo_config: RepoConfig, dataset: pd.DataFrame, online_store_file: FlyteFile
) -> dict:
    inference_data = random.choice(dataset["Hospital Number"])
    logger.info(f"Hospital Number chosen for inference is: {inference_data}")

    entity_rows = [{"Hospital Number": inference_data}]

    FlyteContext.current_context().file_access.get_data(
        online_store_file.download(), ONLINE_STORE_PATH
    )

    feature_vector = (
        FeatureStore(config=repo_config)
        .get_online_features(FEAST_FEATURES, entity_rows)
        .to_dict()
    )

    return feature_vector


# %%
# The following workflow is a separate workflow that can be run indepedently to create features and store them offline.
# This can be run periodically or triggered independently.
@workflow
def featurize(
    repo_config: RepoConfig, imputation_method: str = "mean"
) -> (StructuredDataset, FlyteFile):
    # Load parquet file from sqlite task
    df = load_horse_colic_sql()

    # Perform mean median imputation
    df = mean_median_imputer(dataframe=df, imputation_method=imputation_method)

    # Convert timestamp column from string to datetime.
    converted_df = convert_timestamp_column(dataframe=df, timestamp_column="timestamp")

    online_store_file = store_offline(repo_config=repo_config, dataframe=converted_df)

    return df, online_store_file


# %%
# The following workflow can be run independently to train a model, given the Dataframe, either from Feature store
# or locally:
@workflow
def trainer(
    df: StructuredDataset, num_features_univariate: int = 7
) -> JoblibSerializedFile:
    # Perform univariate feature selection
    selected_features = univariate_selection(
        dataframe=df,  # noqa
        num_features=num_features_univariate,
        data_class=DATA_CLASS,
    )

    # Train the Naive Bayes model
    trained_model = train_model(
        dataset=selected_features,
        data_class=DATA_CLASS,
    )

    return trained_model


# %%
# Finally, we define a workflow that streamlines the whole pipeline building and feature serving process.
# To show how to compose an end to end workflow that includes featurization, training and example predictions,
# we construct the following workflow, composing other workflows:
#
@workflow
def feast_workflow(
    imputation_method: str = "mean",
    num_features_univariate: int = 7,
) -> (JoblibSerializedFile, np.ndarray):
    # Create bucket if it does not already exist
    # & Build feature store
    # build_feature_store(
    #     s3_bucket=create_bucket(bucket_name=s3_bucket),
    #     registry_path=registry_path,
    #     online_store_path=online_store_path,
    # )
    repo_config = create_bucket(bucket_name=S3_BUCKET)

    # Feature engineering
    df, online_store_file = featurize(
        repo_config=repo_config, imputation_method=imputation_method
    )

    # Demonstrate how to load features from offline store
    historical_features = load_historical_features(repo_config=repo_config)

    df >> historical_features

    model = trainer(
        df=historical_features, num_features_univariate=num_features_univariate
    )

    loaded_online_store_file = store_online(
        repo_config=repo_config, online_store_file=online_store_file
    )

    feature_vector = retrieve_online(
        repo_config=repo_config, dataset=df, online_store_file=loaded_online_store_file
    )

    # # Use a feature retrieved from the online store for inference
    predictions = predict(model_ser=model, features=feature_vector)  # noqa

    return model, predictions


if __name__ == "__main__":
    print(f"{feast_workflow()}")

# %%
# You should see prediction against the test input as the workflow output.
