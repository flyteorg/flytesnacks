import pandas as pd
from flytekit.core.artifact import Artifact
from flytekit.core.task import task
from flytekit import ImageSpec
from flytekit.core.workflow import workflow
from typing_extensions import Annotated

"""
Demonstrate a few things
1. Existing workflows produce artifacts. Working with them locally.
  a. flyte://tiny/url
  b. apvdw72f7b4hlt8nhb22/n0/0/o:c

2. I can control the output/naming of the artifacts, and then pull them more easily.
  a. Use an alias

3. I can fetch an artifact and then launch a new execution with it.
  a. The information is embedded in the execution metadata.

4. I can create an artifact locally, and then launch a new execution with it.

5. I can set a query as the default input on another workflow.
"""

flytekit_pr = ImageSpec(
    packages=[
        "git+https://github.com/flyteorg/flytekit.git@465e30bde26390f1e72b9e4ba8213262440be1c4",
        "git+https://github.com/flyteorg/flyteidl.git@c4dc728b600f0072e53938e80a3e4416113bab0a",
    ],
    python_version="3.9",
    apt_packages=["git"],
    registry="ghcr.io/unionai-oss",
)

TaskArtifact = Artifact(name="dataframe_artifact", aliases=["latest"])


@task
def get_plain_df() -> pd.DataFrame:
    return pd.DataFrame({"name": ["Tom", "Joseph"], "age": [20, 22]})


@workflow
def run_get_plain_df():
    get_plain_df()


@task
def print_df(df: pd.DataFrame):
    print("This is the dataframe:")
    print(df)


@workflow
def consume_a_dataframe(df: pd.DataFrame = TaskArtifact.as_query(project="flytesnacks", domain="development")):
    print_df(df=df)


@task
def get_named_df(age: int) -> Annotated[pd.DataFrame, TaskArtifact]:
    return pd.DataFrame({"name": ["Tom", "Joseph"], "age": [age, age]})


@workflow
def run_named_df(age: int):
    get_named_df(age=age)
