import typing
import random
import pandas as pd

from datetime import datetime
from flytekit.core.artifact import Artifact
from flytekit.core.task import task
from flytekit.core.workflow import workflow
from typing_extensions import Annotated
from flytekit import CronSchedule, LaunchPlan
from flytekit.types.file import FlyteFile

"""
ML Style Use Case - Gather data, train models, use models:
This scenario basically mimics three components:

* Tasks or workflows that produce some well-defined data per region, with some time partition.
* A workflow that consumes the outputs of the first workflow at some cadence, and trains a model per region/time.
* A workflow that consumes the model and runs predictions with it.

Scenario:
1. Run the data gather job for a list of regions: SEA, LAX, SFO. This job runs daily and can be re-run to produce
   corrected data for prior days.
2. Fine-tune a model, for each region, using the data from the prior day.
3. Run predictions off of the model
4. Data gather step for SEA, 1/1/2023 is re-run.
5. Re-running the model for SEA, 1/1/2023 should pick up the new changes
"""

# Note:
# the ds partition is formatted as 23_03-7
# Also names and partition keys and values all need to be URL sanitized (see below)
RideCountData = Artifact(name="ride_count_data", partitions={"region": "{{ .inputs.region }}",
                                                             "ds": "{{ .inputs.date }}"})


def get_permutations(s: str) -> typing.List[str]:
    if len(s) <= 1:
        return [s]
    permutations = []
    for i, char in enumerate(s):
        remaining_chars = s[:i] + s[i + 1:]
        for perm in get_permutations(remaining_chars):
            permutations.append(char + perm)

    return permutations


@task
def gather_data(region: str, date: datetime) -> Annotated[pd.DataFrame, RideCountData]:
    """
    This task will produce a dataframe for a given region and date.  The dataframe will be stored in a well-known
    location, and will be versioned by the region and date.
    """
    print(f"Running gather data for region {region} and date {date}")
    fake_neighborhoods = get_permutations(region)
    fake_rides = [random.randint(100, 1000) for _ in range(len(fake_neighborhoods))]
    df = pd.DataFrame({"sectors": fake_neighborhoods, "rides": fake_rides})
    return df


@workflow
def run_gather_data(run_date: datetime):
    regions = ["SEA", "LAX", "SFO"]
    for region in regions:
        gather_data(region=region, date=run_date)


lp_gather_data = LaunchPlan.get_or_create(
    name="scheduled_gather_data_lp",
    workflow=run_gather_data,
    schedule=CronSchedule(
        schedule="* * * * *",  # Run every minute for the demo
        kickoff_time_input_arg="run_date",
    ),
)

# Note:
# Let's say this launch plan is run for 2023-03-01
# You should be able to get the output of the task via this URL
# flyte://project/domain/ride_count_data@<exec-id>
# To retrieve a specific partition, you can append params (note the format of the
# flyte://project/domain/ride_count_data@<exec-id>?region=SEA&ds=23_03-7
# flyte://project/domain/ride_count_data?region=SEA&ds=23_03-7 -> gets the latest one

# @workflow
# def gather_data_and_run_model(region: str, date: datetime):
#     data = gather_data(region=region, date=date)
#     train_model(region=region, data=data)


Model = Annotated[FlyteFile, Artifact(name="my-model", tags=["{{ .inputs.region }}"])]


# Note:
# Using a file in place of an nn.Module for simplicity
# This model will be accessible at flyte://project/domain/my-model@<exec-id>
# If you use flyte://project/domain/my-model, you will get the latest (chronological) artifact.
# What's a tag? I think we should have both a notion of a tag and a version. A tag is a string that can move
# and point to different artifacts over time. A version is a fixed immutable field of the Artifact object.
# To access the latest Model for a given tag, you can use a url like this:
# flyte://project/domain/my-model:SEA


@task
def train_model(region: str, data: pd.DataFrame) -> Model:
    print(f"Training model for region {region} with data {data}")
    return FlyteFile(__file__)


# This query will return the latest artifact for a given region and date.
# Note:
# The ds here is templated from a different source.
data_query = Artifact(name="ride_count_data", partitions={"region": "{{ .inputs.region }}",
                                                          "ds": "{{ .execution.kickoff_time }}"}).as_query()


@workflow
def run_train_model(region: str, data: pd.DataFrame = data_query):
    train_model(region=region, data=data)


# lp_train_model = LaunchPlan.get_or_create(
#     name="scheduled_run_train_model",
#     workflow=run_train_model,
#     schedule=CronSchedule(
#         schedule="0 6 * * *",  # Run daily at 6am
#     ),
# )
# # Note:
# # There is no kickoff time argument here. The partition template will just work off of the execution kick off time.
# # The reactive component of being able to sense the dependency changing and being able to then trigger the training
# # workflow is outside the scope of Artifact service and will be handled by the reactive service.
