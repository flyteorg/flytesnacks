"""
Type Example
------------

``GEType`` when accompanied with data can be used for data validation. It essentially is the type we attach to the data we want to validate.
In this example, we'll implement a simple task, followed by Great Expectations data validation on ``FlyteFile``, and finally, on ``FlyteSchema``.
"""

# %%
# First, let's import the required libraries.
import typing

import pandas as pd
from flytekit import Resources, task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema
from flytekitplugins.greatexpectations import BatchConfig, GEConfig, GEType

# %%
# .. note::
#   ``BatchConfig`` is useful in giving additional batch request parameters to construct both Great Expectations' ``RuntimeBatchRequest`` and ``BatchRequest``.
#   Moreover, there's ``GEConfig`` that encapsulates the essential initialization parameters of the plugin.

# %%
# Next, we define variables that we use throughout the code.
DATASET_REMOTE = "https://raw.githubusercontent.com/superconductive/ge_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
DATA_CONTEXT = "greatexpectations/great_expectations"

# %%
# Simple Type
# ===========
#
# We define a ``GEType`` that checks if the requested ``batch_filter_parameters`` can be used to fetch files from a directory.
# The directory that's being used is defined in ``my_assets``. You can find ``my_assets`` in the Great Expectations config file.
#
# The parameters within the ``data_connector_query`` convey that we're fetching all those files that have "2019" and "01" in the file names.
@task(limits=Resources(mem="500Mi"))
def simple_task(
    directory: GEType[
        str,
        GEConfig(
            data_source="data",
            expectation_suite="test.demo",
            data_connector="my_data_connector",
            batchrequest_config=BatchConfig(
                data_connector_query={
                    "batch_filter_parameters": {
                        "year": "2019",
                        "month": "01",  # noqa: F722
                    },
                },
                limit=10,
            ),
            data_context=DATA_CONTEXT,
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
# First, we define ``GEConfig`` to initialize all our parameters. Here, we're validating a ``FlyteFile``.
ge_config = GEConfig(
    data_source="data",
    expectation_suite="test.demo",
    data_connector="data_flytetype_data_connector",
    local_file_path="/tmp",
    data_context=DATA_CONTEXT,
)

# %%
# Next, we map ``dataset`` parameter to ``GEType``. Under the hood, ``GEType`` validates data in accordance with the ``GEConfig`` defined previously.
# This ``GEConfig`` is being fetched under the name ``ge_config``.
#
# The first value that's being sent within ``GEType`` is ``FlyteFile``. This means that we want to validate the ``FlyteFile`` data.
@task(limits=Resources(mem="500Mi"))
def file_task(
    dataset: GEType[FlyteFile[typing.TypeVar("csv")], ge_config]
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
# We define a ``GEType`` to validate ``FlyteSchema``. The ``local_file_path`` is where we've our parquet file.
@task(limits=Resources(mem="500Mi"))
def schema_task(
    dataframe: GEType[
        FlyteSchema,
        GEConfig(
            data_source="data",
            expectation_suite="test.demo",
            data_connector="data_flytetype_data_connector",
            batchrequest_config=BatchConfig(limit=10),
            local_file_path="/tmp/test.parquet",  # noqa: F722
            data_context=DATA_CONTEXT,
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
# This particular block of code helps us in running the code locally.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print("Simple GE Type...")
    print(simple_wf())
    print("GE Type with FlyteFile...")
    print(file_wf())
    print("GE Type with FlyteSchema...")
    print(schema_wf())
