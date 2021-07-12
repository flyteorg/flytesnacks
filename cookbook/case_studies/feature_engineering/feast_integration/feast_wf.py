"""
Flyte Pipeline with Feast
-------------------------

This workflow makes use of the feature engineering tasks defined in the other file. We'll build an end-to-end Flyte pipeline utilizing "Feast". 

Here the step-by-step process:

* Fetch the SQLite3 data as a data frame
* Perform mean-median-imputation
* Store the updated features in an offline store
* Retrieve the features from an offline store
* Perform univariate-feature-selection
* Train a Naive Bayes model
* Load features into an online store
* Fetch one feature vector for inference
* Generate prediction

.. tip::

    You can simply import the feature engineering tasks, but we use references because we are referring to the existing code.

For Feast to work, make sure ``feature_store.yaml`` file is present in ``feast_repo_path`` workflow input.

.. code-block:: yaml
    :linenos:

    project: feature_engineering
    registry: data/registry.db
    provider: local
    online_store:
        path: data/online_store.db
"""
# %%
# Let's import the libraries.
import logging
import random
import typing
from datetime import datetime, timedelta

import joblib
import pandas as pd
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.feature_store import FeatureStore
from flytekit import Workflow, reference_task, task
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task
from flytekit.types.file import JoblibSerializedFile
from flytekit.types.schema import FlyteSchema
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# %%
# We define the necessary data holders.
logger = logging.getLogger(__file__)
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
# Next, we define the reference tasks. A :py:func:`flytekit.reference_task` references the Flyte tasks that have already been defined, serialized, and registered.
# The primary advantage of using a reference task is to reduce the redundancy; we needn't define the task(s) again if we have multiple datasets that need to be feature-engineered.
@reference_task(
    project="flytesnacks",
    domain="development",
    name="feast_integration.feature_eng_tasks.mean_median_imputer",
    version="v1",
)
def mean_median_imputer(
    dataframe: pd.DataFrame,
    imputation_method: str,
) -> FlyteSchema:
    ...


@reference_task(
    project="flytesnacks",
    domain="development",
    name="feast_integration.feature_eng_tasks.univariate_selection",
    version="v1",
)
def univariate_selection(
    dataframe: pd.DataFrame, num_features: int, data_class: str, feature_view_name: str
) -> pd.DataFrame:
    ...


# %%
# .. note::
#
#   The ``version`` varies depending on the version assigned during the task registration process.

# %%
# We define a task to set the ``dtype`` of the ``timestamp`` column to ``datetime``. 
@task
def set_dtype(df: FlyteSchema, column_name: str) -> FlyteSchema:
    # convert string to datetime in the data frame
    df = df.open().all()
    df[column_name] = pd.to_datetime(df[column_name])
    return df


# %%
# We define two tasks, namely ``store_offline`` and ``retrieve_offline`` to store and retrieve the historial features.
#
# .. list-table:: Decoding the ``Feast`` Jargon
#    :widths: 25 25
#
#    * - ``FeatureStore``
#      - A FeatureStore object is used to define, create, and retrieve features.
#    * - ``Entity``
#      - Represents a collection of entities and associated metadata. It's usually the primary key of your data.
#    * - ``FeatureView``
#      - A FeatureView defines a logical grouping of serveable features.
#    * - ``FileSource``
#      - File data sources allow for the retrieval of historical feature values from files on disk for building training datasets, as well as for materializing features into an online store.
#    * - ``fs.apply()``
#      - Register objects to metadata store and update related infrastructure.
#    * - ``get_historical_features()``
#      - Enrich an entity dataframe with historical feature values for either training or batch scoring.
@task
def store_offline(dataframe: FlyteSchema, repo_path: str) -> (str, str):
    fs = FeatureStore(repo_path=repo_path)
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


@task
def retrieve_offline(repo_path: str) -> pd.DataFrame:
    fs = FeatureStore(repo_path=repo_path)
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

    retrieval_job = fs.get_historical_features(
        entity_df=entity_df,
        feature_refs=FEAST_FEATURES,
    )

    feature_data = retrieval_job.to_df()
    return feature_data


# %%
# Next, we train the Naive Bayes model using the data that's been fetched from the feature store.
@task
def train_model(
    dataset: pd.DataFrame, data_class: str, feature_view_name: str
) -> JoblibSerializedFile:
    X_train, _, y_train, _ = train_test_split(
        dataset,
        dataset[feature_view_name + "__" + data_class],
        test_size=0.33,
        random_state=42,
    )
    model = GaussianNB()
    model.fit(X_train, y_train)
    model.feature_names = list(X_train.columns.values)
    fname = "model.joblib.dat"
    joblib.dump(model, fname)
    return fname


# %%
# To perform inferencing, we define two tasks: ``store_online`` and ``retrieve_online``.
#
# .. list-table:: Decoding the ``Feast`` Jargon
#    :widths: 25 25
#
#    * - ``materialize()``
#      - Materialize data from the offline store into the online store.
#    * - ``get_online_features()``
#      - Retrieves the latest online feature data.
#
# .. note::
#   One key difference between the online store and data source is that only the latest feature values are stored per entity key. No historical values are stored.
#   Our dataset has two such entries with the same ``Hospital Number`` but different time stamps. Only data point with the latest timestamp is picked from the online store.
@task
def store_online(repo_path: str) -> str:
    store = FeatureStore(repo_path=repo_path)
    store.materialize(
        start_date=datetime.utcnow() - timedelta(days=50),
        end_date=datetime.utcnow() - timedelta(minutes=10),
    )
    return repo_path


@task
def retrieve_online(
    repo_path: str, dataset: pd.DataFrame
) -> typing.Dict[str, typing.List[str]]:
    store = FeatureStore(repo_path=repo_path)
    feature_refs = FEAST_FEATURES

    inference_data = random.choice(dataset["Hospital Number"])
    logger.info(f"Hospital Number chosen for inference is: {inference_data}")

    entity_rows = [{"Hospital Number": inference_data}]

    online_response = store.get_online_features(feature_refs, entity_rows)
    online_response_dict = online_response.to_dict()
    return online_response_dict


# %%
# We define a task to test the model using the inference point fetched earlier.
@task
def test_model(
    model_ser: JoblibSerializedFile,
    inference_point: typing.Dict[str, typing.List[str]],
) -> typing.List[str]:

    # Load model
    model = joblib.load(model_ser)
    f_names = model.feature_names

    test_list = []
    for each_name in f_names:
        test_list.append(inference_point[each_name][0])
    prediction = model.predict([test_list])
    return prediction


# %%
# Finally we define the workflow that streamlines the whole pipeline building and feature serving process.
# We're using an ``imperative-style workflow`` to convert the step-by-step text into Flyte-compatible pipeline.
wb = Workflow(name="feast_integration.workflow.fe_wf")
wb.add_workflow_input("imputation_method", str)
wb.add_workflow_input("feast_repo_path", str)
wf_in = wb.add_workflow_input("num_features_univariate", int)

sql_task = SQLite3Task(
    name="sqlite3.horse_colic",
    query_template="select * from data",
    output_schema_type=FlyteSchema,
    task_config=SQLite3Config(
        uri=DATABASE_URI,
        compressed=True,
    ),
)

node_t1 = wb.add_entity(sql_task)

node_t2 = wb.add_entity(
    mean_median_imputer,
    dataframe=node_t1.outputs["results"],
    imputation_method=wb.inputs["imputation_method"],
)

node_t3 = wb.add_entity(set_dtype, df=node_t2.outputs["o0"], column_name="timestamp")

node_t4 = wb.add_entity(
    store_offline,
    dataframe=node_t3.outputs["o0"],
    repo_path=wb.inputs["feast_repo_path"],
)
node_t5 = wb.add_entity(retrieve_offline, repo_path=node_t4.outputs["o0"])

node_t6 = wb.add_entity(
    univariate_selection,
    dataframe=node_t5.outputs["o0"],
    data_class=DATA_CLASS,
    num_features=wf_in,
    feature_view_name=node_t4.outputs["o1"],
)

node_t7 = wb.add_entity(
    train_model,
    dataset=node_t6.outputs["o0"],
    data_class=DATA_CLASS,
    feature_view_name=node_t4.outputs["o1"],
)

node_t8 = wb.add_entity(store_online, repo_path=node_t4.outputs["o0"])
node_t9 = wb.add_entity(
    retrieve_online, repo_path=node_t8.outputs["o0"], dataset=node_t1.outputs["results"]
)

node_t10 = wb.add_entity(
    test_model,
    model_ser=node_t7.outputs["o0"],
    inference_point=node_t9.outputs["o0"],
)

wb.add_workflow_output(
    "output_from_t10", node_t10.outputs["o0"], python_type=typing.List[str]
)

if __name__ == "__main__":

    wb(imputation_method="mean", num_features_univariate=7, feast_repo_path=".")

# %%
# You should see prediction against the test input as the workflow output.
