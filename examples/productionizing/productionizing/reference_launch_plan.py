# Reference launch plan

# A `flytekit.reference_launch_plan` references previously defined, serialized,
# and registered Flyte launch plans.
# You can reference launch plans from other projects and create workflows
# that use launch plans declared by others.

# The following example illustrates how to use reference launch plans
from typing import List

from flytekit import reference_launch_plan, workflow
from flytekit.types.file import FlyteFile


@reference_launch_plan(
    project="flytesnacks",
    domain="development",
    name="data_types_and_io.file.normalize_csv_file",
    version="{{ registration.version }}",
)
def normalize_csv_file(
    csv_url: FlyteFile,
    column_names: List[str],
    columns_to_normalize: List[str],
    output_location: str,
) -> FlyteFile:
    ...


@workflow
def reference_lp_wf() -> FlyteFile:
    return normalize_csv_file(
        csv_url="https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv",
        column_names=["Name", "Sex", "Age", "Heights (in)", "Weight (lbs)"],
        columns_to_normalize=["Age"],
        output_location="",
    )
