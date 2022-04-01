"""
KNN Classifier
--------------

In this example, let's understand how effortlessly the Modin DataFrames can be used with tasks and workflows in a simple classification pipeline.
Modin uses [Ray](https://github.com/ray-project/ray/) or [Dask](https://dask.org/) as the compute engine. We'll use Ray in this example.

To install Modin with Ray as the backend,

.. code:: bash

    pip install modin[ray]

.. note

    To install Modin with Dask as the backend,

    .. code:: bash

       pip install modin[dask]

Let's dive right in!
"""
# %%
# Let's import the necessary dependencies.
from typing import List, NamedTuple

import flytekitplugins.modin
import modin.pandas
import ray
from flytekit import task, workflow
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ray.shutdown()  # close previous instance of ray (if any)
ray.init()  # open a new instance of ray


split_data = NamedTuple(
    "split_data",
    train_features=modin.pandas.DataFrame,
    test_features=modin.pandas.DataFrame,
    train_labels=modin.pandas.DataFrame,
    test_labels=modin.pandas.DataFrame,
)


# %%
# We define a task that processes the iris dataset after loading it into the environment.
@task
def data_processing() -> split_data:
    # load iris Data
    iris = load_iris()

    # convert features and target (numpy arrays) into Modin DataFrames
    iris_features = modin.pandas.DataFrame(data=iris.data, columns=iris.feature_names)
    iris_target = modin.pandas.DataFrame(data=iris.target, columns=["species"])

    # split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        iris_features, iris_target, test_size=0.33, random_state=101
    )

    return split_data(
        train_features=X_train,
        test_features=X_test,
        train_labels=y_train,
        test_labels=y_test,
    )


# %%
# Next, we define a task that:
#
# 1. trains a KNeighborsClassifier model,
# 2. fits the model to the data, and
# 3. predicts the output for the test dataset.
@task
def fit_and_predict(
    X_train: modin.pandas.DataFrame,
    X_test: modin.pandas.DataFrame,
    y_train: modin.pandas.DataFrame,
) -> List[int]:
    lr = KNeighborsClassifier()  # create a KNeighborsClassifier model
    lr.fit(X_train, y_train)  # fit the model to the data
    predicted_vals = lr.predict(X_test)  # predict values for test data
    return predicted_vals.tolist()


# %%
# We compute accuracy of the model.
@task
def calc_accuracy(
    y_test: modin.pandas.DataFrame, predicted_vals_list: List[int]
) -> float:
    return accuracy_score(y_test, predicted_vals_list)


# %%
# Lastly, we define a workflow.
@workflow
def pipeline() -> float:
    split_data_vals = data_processing()
    predicted_vals_output = fit_and_predict(
        X_train=split_data_vals.train_features,
        X_test=split_data_vals.test_features,
        y_train=split_data_vals.train_labels,
    )
    return calc_accuracy(
        y_test=split_data_vals.test_labels, predicted_vals_list=predicted_vals_output
    )


if __name__ == "__main__":
    print(f"Accuracy of the model is {pipeline()}%")
