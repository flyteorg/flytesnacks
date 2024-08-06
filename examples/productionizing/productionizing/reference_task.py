from typing import List, NamedTuple

from flytekit import StructuredDataset, reference_task, workflow
from flytekit.types.file import FlyteFile

# A `flytekit.reference_task` references the Flyte tasks that have already been defined, serialized, and registered.
# You can reference tasks from other projects and create workflows that use tasks declared by others.
# These tasks can be in their own containers, python runtimes, flytekit versions, and even different languages.

# The following example illustrates how to use reference tasks
# Note that reference tasks cannot be run locally. You must mock them out


@reference_task(
    project="flytesnacks",
    domain="development",
    name="data_types_and_io.file.normalize_columns",
    version="{{ registration.version }}",
)
def normalize_columns(
    csv_url: FlyteFile,
    column_names: List[str],
    columns_to_normalize: List[str],
    output_location: str,
) -> FlyteFile:
    ...


outputs = NamedTuple("Outputs", results=StructuredDataset)


@reference_task(
    project="flytesnacks",
    domain="development",
    name="bigquery",
    version="{{ registration.version }}",
)
def bigquery_task(version: int) -> outputs:
    ...


@workflow
def wf() -> FlyteFile:
    bigquery_task(version=1)
    return normalize_columns(
        csv_url="https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv",
        column_names=["Name", "Sex", "Age", "Heights (in)", "Weight (lbs)"],
        columns_to_normalize=["Age"],
        output_location="",
    )
