"""
Linear Regression Using Modin Dataframe
----------------------------------------

In this example, let's implement Linear Regression using the Modin DataFrame.

.. note::

   We use Ray as the backend in this case.

Installation
^^^^^^^^^^^^^

To install Modin with Ray as the backend,

.. code:: bash

   pip install modin[ray]


To install Modin with Dask as the backend,

.. code:: bash

   pip install modin[dask]

Let's dive into the example.
"""
# %%
# Import the necessary dependencies
import typing
from types import ModuleType
from typing import List, Tuple

import flytekitplugins.modin
import modin.pandas
import numpy as np
import ray
from flytekit import task, workflow
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

ray.shutdown()
ray.init()

# A function that converts a column of integers to strings based on certain conditions.
def converter(specie):
    if specie == 0:
        return "setosa"
    elif specie == 1:
        return "versicolor"
    else:
        return "virginica"


# %%
# We define a task that processes the iris dataset (after loading it into the environment).
@task
def data_processing() -> (
    modin.pandas.DataFrame,
    modin.pandas.DataFrame,
    modin.pandas.DataFrame,
):
    # load Iris Data
    iris = load_iris()
    # creating modin DataFrames
    iris_df = modin.pandas.DataFrame(data=iris.data, columns=iris.feature_names)
    # separate the features and target columns
    target_df = modin.pandas.DataFrame(data=iris.target, columns=["species"])
    target_df["species"] = target_df["species"].apply(converter)
    # concatenate the DataFrames
    iris_df = modin.pandas.concat([iris_df, target_df], axis=1)
    # convert objects to numeric type
    iris_df.drop("species", axis=1, inplace=True)
    target_df = modin.pandas.DataFrame(columns=["species"], data=iris.target)
    iris_df = modin.pandas.concat([iris_df, target_df], axis=1)
    # the features and target un two separate modin DataFrames
    irisData_features = iris_df.drop(labels="sepal length (cm)", axis=1)
    irisData_target = iris_df["sepal length (cm)"]

    # split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        irisData_features, irisData_target, test_size=0.33, random_state=101
    )
    y_train = modin.pandas.DataFrame(y_train)
    return X_train, X_test, y_train


# %%
# Next, let's define a task that:
#
# 1. Trains a LinearRegression model,
# 2. Fits the model to the data,
# 3. Predicts the output for the test dataset.


@task
def train_fit_predict(
    X_train: modin.pandas.DataFrame,
    X_test: modin.pandas.DataFrame,
    y_train: modin.pandas.DataFrame,
) -> np.ndarray:
    lr = LinearRegression()  # create LinearRegression model
    lr.fit(X_train, y_train)  # fit the model to the data
    predicted_vals = lr.predict(X_test)  # predict values for test data
    return predicted_vals


# %%
# Lastly, we define a workflow.
@workflow
def pipeline() -> np.ndarray:
    X_train, X_test, y_train = data_processing()
    return train_fit_predict(X_train=X_train, X_test=X_test, y_train=y_train)


if __name__ == "__main__":
    print(f"Predicted vs. actual sepal length (cm) is {pipeline()[0]} and {'5.6'}")

# %%
# Conclusion
# ^^^^^^^^^^^
#
# We learned how to use Modin DataFrame to implement Linear Regression on the Iris dataset.
