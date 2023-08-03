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
6. Re-running predictions should pick up the new model.
7. Re-running predictions on a different set of inputs, but using the model from step 3.
"""

# Note:
# the ds partition is formatted as 23_03-7
# Also names and partition keys and values all need to be URL sanitized (see below)
RideCountData = Artifact(name="ride_count_data", partition={"region": "{{ .inputs.region }}",
                                                            "ds": "{{ .inputs.date[%YY_%MM-%dd] }}"})


@task
def gather_data(region: str, date: datetime) -> Annotated[pd.DataFrame, RideCountData]:
    """
    This task will produce a dataframe for a given region and date.  The dataframe will be stored in a well-known
    location, and will be versioned by the region and date.
    """
    ...


@workflow
def run_gather_data(run_date: datetime):
    regions = ["SEA", "LAX", "SFO"]
    for region in regions:
        gather_data(region, run_date)


lp_gather_data = LaunchPlan.get_or_create(
    name="scheduled_gather_data_lp",
    workflow=run_gather_data,
    schedule=CronSchedule(
        schedule="0 0 * * *",  # Run daily at midnight
        kickoff_time_input_arg="run_date",
    ),
)

# Note:
# Let's say this launch plan is run for 2023-03-01
# You should be able to get the output of the task via this URL
# flyte://project/domain/ride_count_data:<exec-id>
# To retrieve a specific partition, you can append params (note the format of the
# flyte://project/domain/ride_count_data:<exec-id>?region=SEA&ds=23_03-7
# flyte://project/domain/ride_count_data?region=SEA&ds=23_03-7 -> gets the latest one

# Note:
# Users should be able to add additional tags/versions to an existing artifact.
# Effectively "cp" flyte://project/domain/ride_count_data:<exec-id> flyte://project/domain/ride_count_data:mytstver1


Model = Annotated[nn.Module, Artifact(name="my-model", version="myver")]
# Note:
# This model will be accessible at flyte://project/domain/my-model:<exec-id>
# If you use flyte://project/domain/my-model, you will get the latest (chronological) artifact.


@task
def train_model(region: str, data: pd.DataFrame) -> Model:
    ...


# This query will return the latest artifact for a given region and date.
# Note:
# The ds here is templated from a different source.
data_query = Artifact.query(name="ride_count_data", partition={"region": "{{ .inputs.region }}",
                                                               "ds": "{{ .execution.kickoff_time[%YY_%MM-%dd] }}"})


@workflow
def run_train_model(region: str, data: pd.DataFrame = data_query):
    train_model(region=region, data=data)


lp_train_model = LaunchPlan.get_or_create(
    name="scheduled_run_train_model",
    workflow=run_train_model,
    schedule=CronSchedule(
        schedule="0 6 * * *",  # Run daily at 6am
    ),
)
# Note:
# There is no kickoff time argument here. The partition template will just work off of the execution kick off time.
# The reactive component of being able to sense the dependency changing and being able to then trigger the training
# workflow is outside the scope of Artifact service and will be handled by the reactive service.


@task
def predictions(model: FlyteFile):
    print(f"This is my model {model}")


Artifact.query(uri="flyte://...")
Artifact.query(name="my-model", version="some-exec-id")




def t1 () -> Model:
  ...

def t2 (a: Artifact):
    ...



@workflow
def run_predictions(model: FlyteFile = Artifact.query(name="my-model")):
    predictions(model=model)

