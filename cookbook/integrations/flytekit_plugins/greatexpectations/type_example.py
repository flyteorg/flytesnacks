"""
Type Example
------------

``GreatExpectationsType`` when accompanied with data can be used for data validation. 
It essentially is the type we attach to the data we want to validate.
In this example, we'll implement a simple task, followed by Great Expectations data validation on ``FlyteFile``, and finally, on ``FlyteSchema``.
"""

# %%
# First, let's import the required libraries.
import typing

import pandas as pd
from flytekit import Resources, task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema
from flytekitplugins.great_expectations import (
    BatchRequestConfig,
    GreatExpectationsFlyteConfig,
    GreatExpectationsType,
)

# %%
# .. note::
#   ``BatchRequestConfig`` is useful in giving additional batch request parameters to construct both Great Expectations' 
#   ``RuntimeBatchRequest`` and ``BatchRequest``.
#   Moreover, there's ``GreatExpectationsFlyteConfig`` that encapsulates the essential initialization parameters of the plugin.

# %%
# Next, we define variables that we use throughout the code.
DATASET_REMOTE = "https://raw.githubusercontent.com/superconductive/ge_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
CONTEXT_ROOT_DIR = "greatexpectations/great_expectations"

# %%
# Simple Type
# ===========
#
# We define a ``GreatExpectationsType`` that checks if the requested ``batch_filter_parameters`` can be used to fetch files from a directory.
# The directory that's being used is defined in ``my_assets``. You can find ``my_assets`` in the Great Expectations config file.
#
# The parameters within the ``data_connector_query`` convey that we're fetching all those files that have "2019" and "01" in the file names.
@task(limits=Resources(mem="500Mi"))
def simple_task(
    directory: GreatExpectationsType[
        str,
        GreatExpectationsFlyteConfig(
            data_source="data",
            expectation_suite="test.demo",
            data_connector="my_data_connector",
            batchrequest_config=BatchRequestConfig(
                data_connector_query={
                    "batch_filter_parameters": {
                        "year": "2019",
                        "month": "01",  # noqa: F722
                    },
                    "limit": 10,
                },
            ),
            context_root_dir=CONTEXT_ROOT_DIR,
        ),
    ]
) -> str:
    return f"Validation works for {directory}!"


# %%
# Finally, we define a workflow to call our task.
@workflow
def simple_wf(directory: str = "my_assets") -> str:
    return simple_task(directory=directory)


# %%
# FlyteFile
# =========
#
# First, we define ``GreatExpectationsFlyteConfig`` to initialize all our parameters. Here, we're validating a ``FlyteFile``.
great_expectations_config = GreatExpectationsFlyteConfig(
    data_source="data",
    expectation_suite="test.demo",
    data_connector="data_flytetype_data_connector",
    local_file_path="/tmp",
    context_root_dir=CONTEXT_ROOT_DIR,
)

# %%
# Next, we map ``dataset`` parameter to ``GreatExpectationsType``. 
# Under the hood, ``GreatExpectationsType`` validates data in accordance with the ``GreatExpectationsFlyteConfig`` defined previously.
# This ``GreatExpectationsFlyteConfig`` is being fetched under the name ``great_expectations_config``.
#
# The first value that's being sent within ``GreatExpectationsType`` is ``FlyteFile``. 
# This means that we want to validate the ``FlyteFile`` data.
@task(limits=Resources(mem="500Mi"))
def file_task(
    dataset: GreatExpectationsType[FlyteFile[typing.TypeVar("csv")], great_expectations_config]
) -> pd.DataFrame:
    return pd.read_csv(dataset)


# %%
# Next, we define a workflow to call our task.
@workflow
def file_wf() -> pd.DataFrame:
    return file_task(dataset=DATASET_REMOTE)


# %%
# FlyteSchema
# ===========
#
# We define a ``GreatExpectationsType`` to validate ``FlyteSchema``. The ``local_file_path`` is where we've our parquet file.
@task(limits=Resources(mem="500Mi"))
def schema_task(
    dataframe: GreatExpectationsType[
        FlyteSchema,
        GreatExpectationsFlyteConfig(
            data_source="data",
            expectation_suite="test.demo",
            data_connector="data_flytetype_data_connector",
            batchrequest_config=BatchRequestConfig(data_connector_query={"limit": 10}),
            local_file_path="/tmp/test.parquet",  # noqa: F722
            context_root_dir=CONTEXT_ROOT_DIR,
        ),
    ]
) -> int:
    return dataframe.shape[0]


# %%
# Finally, we define a workflow to call our task.
# We're using DataFrame returned by the ``file_task`` that we defined in the ``FlyteFile`` section.
@workflow
def schema_wf() -> int:
    return schema_task(dataframe=file_wf())


# %%
# Lastly, this particular block of code helps us in running the code locally.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print("Simple GreatExpectations Type...")
    print(simple_wf())
    print("GreatExpectations Type with FlyteFile...")
    print(file_wf())
    print("GreatExpectations Type with FlyteSchema...")
    print(schema_wf())
