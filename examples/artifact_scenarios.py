import pandas as pd
from datetime import datetime
from flytekit.core.artifact import Artifact
from flytekit.core.task import task
from flytekit.core.workflow import workflow
from typing_extensions import Annotated

"""
Two important points from the chat with Mick:
* The notion of different parts of the same dataset is important enough that we should elevate this to a 
  citizen in Artifact.
* The labeling of the various partitions of Artifacts should be templated, and filled in from a the following sources:
  * The inputs to the task or workflow
    e.g. `{{ .inputs.region }}`
  * Elements of the workflow execution
    e.g. `{{ .execution.name }}` or `{{ .execution.triggered_time }}`
    
One important point from the internal meeting:
* Run-time lineage information may not be sufficient.  

# Three high level user situations motivated here in this file.
#  - Get data along some dimensions, train a model on it, and use the model.
#  - Orchestration of a couple queries, and backfilling of data.
#  - Users uploading data and then using the data to kick off workflows.

Use Case 1 - Gather data, train models, use models:
This scenario basically mimics three components:

* Tasks or workflows that produce some well-defined data per region, with some time partition.
* A workflow that consumes the outputs of the first workflow at some cadence, and trains a model per region/time.
* A workflow that consumes the model and runs predictions with it.

Scenario:
1. Run the data gather for SEA, and 1/1/2023.
2. Run the model
3. Run predictions off of the model
4. Data gather step for SEA, 1/1/2023 is re-run.
5. Re-running the model for SEA, 1/1/2023 should pick up the new changes
6. Re-running predictions should pick up the new model.
7. Re-running predictions on a different set of inputs, but using the model from step 3.

Open questions:
* artifact project/domain, is this separate from the execution
* additional dimensions
* rough idea on lineage and extracting out the source
* static tracking of artifacts to their sources

What are the types of lineages that are possible?
* Lineage across executions, or uploads
  - For a named Artifact, show me all materializations.
  - For a given Artifact, show me all the executions that used it, and the artifacts at that point in time.
* Lineage across dependencies
  - If Task A (input_a) -> Task B (input_b) -> Task C (input_c) -> output_c
    This relationship should be knowable in advance, right after registration before any runs are done. 

"""

TaskArtifact = Artifact(name="dataframe_artifact", "latest")


# should be okay either way. Admin knows at execution time what the project and domain are, and can fill it in.
Artifact.query(project="p", domain="d")  # and other args

# If task looks like
# def gather_data(region: str, day: datetime): ...

# Would need to be able to template inputs as part of the partition query. Would also
# need to template inputs at specification time.
# Should we call this tag or version? Tag makes more sense if we want it overrideable by default.
# Version makes more sense if it's immutable and "latest" is just some special hard-coded thing.
PartitionedTaskArtifact = Artifact(name="ride_count_data", partition={"region": "{{ .inputs.region }}",
                                                                      "day": "2023-01-01"}, version="importantv1")
# region=SEA
# flyte://project/domain/ride_count_data:importantv1?region=SEA&day=2023-01-01
# Tags are unique on (project/domain/name) but can change across time, if the workflow is re-run. In this case here,
# if the task or workflow is run twice, after the second run, this URI will return the second run's output.

PartitionedTaskArtifact2 = Artifact(name="ride_count_data", partition={"region": "LAX",
                                                                       "day": "{{ .inputs.day[%YY_%MM-%dd] }}"})
# region=LAX, day=2023-01-01
# flyte://project/domain/ride_count_data:<exec-id>?region=SEA&day=23-01-1

# unnamed artifact, how to access the data?
# region=LAX, day=2023-01-01
# flyte://project/domain/<exec-id>/nodeid/retry/o0:(exec-id) is the tag, but empty tag should default to latest


# All unnamed artifacts by default are non-partitioned. (In the future we can think about picking up partitioned
# structured datasets for instance automatically.)

PartitionedTaskArtifact2 = Artifact(name="dataframe_artifact", partition={"region": "LAX",
                                                                         "day": "20230515"},
                                    "constant_str")

PartitionedTaskArtifact2 = Artifact(name="dataframe_artifact", partition={"region": "LAX",
                                                                         "day": "20230515"},
                                    version_tag="exec-id-from517")

Artifact.query(name="ride_count_data", partition={"region": "SEA", "day": "2023-01-01"}, tag="importantv1")


PartitionedTaskArtifact3 = Artifact(name="dataframe_artifact", partitions=["region", "day"], "latest")

Artifact.query(name="ride_count_data", partition={"region": "SEA", "day": "2023-01-01"})

# Question - if you have an alias, does that point to a specific partition? Or does it just refer
# to the artifact as a whole. How do you specify it as a url?


# Partitions and whole data should be accessible via a unique url
# flyte://project/domain/ride_count_data:mytst1?region=SEA&day=2023-01-01

# If an artifact is explicitly named, all executions of it should be related to each other.


"""

maybe:
change the artifact service and the get data endpoint, don't store every single output, only store it on request.
change get data to only work with outputs, not inputs.
force it to have a name? likely no, because if you force it to have a name, that implies user interference.

If artifact is not named, what is the cross section a user would want to see? None.

"""


@task
def gather_data(region: str, day: datetime) -> Annotated[pd.DataFrame, ]:
    return pd.DataFrame({"name": ["Tom", "Joseph"], "age": [20, 22]})


@workflow
def run_gather_data(region: str, day: datetime):
    gather_data(region=region, day=day)


@task
def print_df(df: pd.DataFrame):
    print("This is the dataframe:")
    print(df)

"""
Artifacts are strange in that they are just named pointers.
They're like github tags can move across time.

Scenario 2 - ETL:
1. Two query tasks run, one after the other (this dependency is set).
2. The queries both take a date parameter as input. Run them across time and run a backfill scenario. 
"""


@workflow
def consume_a_dataframe(df: pd.DataFrame = TaskArtifact.as_query(project="flytesnacks", domain="development")):
    print_df(df=df)


@task
def get_named_df(age: int) -> Annotated[pd.DataFrame, TaskArtifact]:
    return pd.DataFrame({"name": ["Tom", "Joseph"], "age": [age, age]})


@workflow
def run_named_df(age: int):
    get_named_df(age=age)
