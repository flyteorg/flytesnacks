import pandas as pd
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression

from flytekit import task, workflow
from flytekit.types.pickle import FlytePickle


# 🧱 @task decorators define the building blocks of your pipeline
@task
def get_data() -> pd.DataFrame:
    """Get the wine dataset."""
    return load_wine(as_frame=True).frame


@task
def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Simplify the task from a 3-class to a binary classification problem."""
    return data.assign(target=lambda x: x["target"].where(x["target"] == 0, 1))


@task
def train_model(data: pd.DataFrame, hyperparameters: dict) -> FlytePickle:
    """Train a model on the wine dataset."""
    features = data.drop("target", axis="columns")
    target = data["target"]
    return LogisticRegression(**hyperparameters).fit(features, target)


# 🔀 @workflows decorators define the flow of data through the tasks
@workflow
def training_workflow() -> FlytePickle:
    """Put all of the steps together into a single workflow."""
    data = get_data()
    processed_data = process_data(data=data)
    return train_model(data=processed_data, hyperparameters={"max_iter": 5000})


if __name__ == "__main__":
    # You can run this script with pre-defined arguments with `python flyte_workflow.py`
    # but we recommend running it with the `pyflyte run` CLI command, as you'll see in
    # the next step of this walkthrough.
    print(f"Running training_workflow() {training_workflow()}")
