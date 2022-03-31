"""
Linear Regression With Modin
-----------------------------

In this example, let's understand how effortlessly the Modin DataFrames can be used within Flyte tasks and workflows in a linear regression pipeline.

Modin uses [Ray](https://github.com/ray-project/ray/) or [Dask](https://dask.org/) as the compute engine. We'll use Ray in this example. 


.. note

    To install Modin with Ray as the backend,

    .. code:: bash

       pip install modin[ray]


    To install Modin with Dask as the backend,

    .. code:: bash

       pip install modin[dask]

Let's dive into the example.
"""
# %%
# Import the necessary dependencies.
import typing
from typing import List, NamedTuple, Tuple

import flytekitplugins.modin
import modin.pandas
import numpy as np
import ray
from flytekit import task, workflow
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

ray.shutdown()  # close previous instance of ray (if any)
ray.init()  # open a new instance of ray


split_data = typing.NamedTuple(
    "split_data",
    o1=modin.pandas.DataFrame,
    o2=modin.pandas.DataFrame,
    o3=modin.pandas.DataFrame,
    o4=modin.pandas.DataFrame,
)


# %%
# Next, we define a task that processes the iris dataset after loading it into the environment.
@task
def data_processing() -> split_data:
    # load Iris Data
    iris = load_iris()

    # convert features and target (numpy array) into Modin DataFrames
    iris_df = modin.pandas.DataFrame(data=iris.data, columns=iris.feature_names)
    target_df = modin.pandas.DataFrame(data=iris.target, columns=["species"])

    # concatenate all the columns
    iris_df = modin.pandas.concat([iris_df, target_df], axis=1)

    # the features and target in two separate Modin DataFrames
    iris_features = iris_df.drop(labels="sepal length (cm)", axis=1)  # make snake case
    iris_target = modin.pandas.DataFrame(iris_df["sepal length (cm)"])

    # split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        iris_features, iris_target, test_size=0.33, random_state=101
    )
    y_train = modin.pandas.DataFrame(y_train)
    return X_train, X_test, y_train, y_test


# %%
# Next, let's define a task that:
#
# 1. Trains a LinearRegression model,
# 2. Fits the model to the data,
# 3. Predicts the output for the test dataset.
@task
def fit_and_predict(
    X_train: modin.pandas.DataFrame,
    X_test: modin.pandas.DataFrame,
    y_train: modin.pandas.DataFrame,
) -> typing.List[typing.List[float]]:
    lr = LinearRegression()  # create LinearRegression model
    lr.fit(X_train, y_train)  # fit the model to the data
    predicted_vals = lr.predict(X_test)  # predict values for test data
    predicted_vals_list = predicted_vals.tolist()
    return predicted_vals_list


# %%
# Now, we compute the accuracy of the model using Mean Absolute Error, Mean Squared Error, and Mean Root Squared Error.
@task
def calc_accuracy(
    y_test: modin.pandas.DataFrame, predicted_vals_list: typing.List[typing.List[float]]
) -> List[float]:
    return [
        mean_absolute_error(y_test, predicted_vals_list),
        mean_squared_error(y_test, predicted_vals_list),
        np.sqrt(mean_squared_error(y_test, predicted_vals_list)),
    ]


# %%
# Lastly, we define a workflow.
@workflow
def pipeline() -> List[float]:
    X_train, X_test, y_train, y_test = data_processing()
    predicted_vals_output = fit_and_predict(
        X_train=X_train, X_test=X_test, y_train=y_train
    )
    return calc_accuracy(y_test=y_test, predicted_vals_list=predicted_vals_output)


if __name__ == "__main__":
    print(
        f"Metrics to determine accuracy: Mean Absolute Error, Mean Squared Error, Mean Root Squared Error are: {pipeline()} "
    )
