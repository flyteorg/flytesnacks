"""
Predicting House Price in Multiple Regions Using XGBoost and Dynamic Workflows
-------------------------------------------------------------------------------
`XGBoost <https://xgboost.readthedocs.io/en/latest/>`__ is an optimized distributed gradient boosting library designed to be efficient, flexible, and portable. 
It uses `gradient boosting <https://en.wikipedia.org/wiki/Gradient_boosting>`__ technique to implement Machine Learning algorithms.

In this tutorial, we will understand how to predict house prices in multiple regions using XGBoost, and dynamic workflows in Flyte.

A dynamic workflow is a typical workflow where the users can perform any arbitrary computation by consuming the inputs and producing the outputs. In the backend, it is designed as a task. During execution, the function body can be run to produce a workflow.

We will split the generated dataset into train, test and validation set. 

Next, we will create two dynamic workflows in Flyte, that will:

1. Generate and split the data for multiple regions.

2. Train the model using XGBoost and generate predictions.

We can use two separate methods to fit the model and generate predictions, but incorporating a workflow will perform both the tasks in parallel, which is efficient and powerful.

Let's get started with the example!
"""

# %%
# First, let's import the required packages into the environment.
import typing

import pandas as pd
from flytekit import Resources, dynamic, workflow

# %%
# We define a ``try-catch`` block to import data preprocessing functions from the :ref:`single_region_house_prediction`.
try:
    from .house_price_predictor import (
        generate_and_split_data,
        fit,
        predict,
    )
except ImportError:
    from house_price_predictor import (
        generate_and_split_data,
        fit,
        predict,
    )

# %%
# We initialize variables that represent columns in the dataset. We use these variables to build the model, since they affect the house prices.
NUM_HOUSES_PER_LOCATION = 1000
COLUMNS = [
    "PRICE",
    "YEAR_BUILT",
    "SQUARE_FEET",
    "NUM_BEDROOMS",
    "NUM_BATHROOMS",
    "LOT_ACRES",
    "GARAGE_SPACES",
]
# initialize location names to predict house prices in these regions.
LOCATIONS = [
    "NewYork_NY",
    "LosAngeles_CA",
    "Chicago_IL",
    "Houston_TX",
    "Dallas_TX",
    "Phoenix_AZ",
    "Philadelphia_PA",
    "SanAntonio_TX",
    "SanDiego_CA",
    "SanFrancisco_CA",
]

# %%
# Data Generation and Preprocessing 
# ====================================
#
# We call the :ref:`data generation <Data Generation>` and :ref:`data preprocessing <Data Preprocessing and Splitting>` to generate and split the data. We return the result as DataFrames.
# Now, let's create a ``NamedTuple`` that maps variable names to their respective data type.
dataset = typing.NamedTuple(
    "GenerateSplitDataOutputs",
    train_data=typing.List[pd.DataFrame],
    val_data=typing.List[pd.DataFrame],
    test_data=typing.List[pd.DataFrame],
)

# %%
# Next, we create a :py:func:`~flytekit:flytekit.dynamic` workflow to generate and split the data for multiple regions.
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def generate_and_split_data_multiloc(
    locations: typing.List[str],
    number_of_houses_per_location: int,
    seed: int,
) -> dataset:
    train_sets = [] # create empty lists for train, validation, and test subsets
    val_sets = []
    test_sets = []
    for _ in locations:
        _train, _val, _test = generate_and_split_data(
            number_of_houses=number_of_houses_per_location, seed=seed
        )
        train_sets.append(
            _train,
        )
        val_sets.append(
            _val,
        )
        test_sets.append(
            _test,
        )
    # split the dataset into train, validation, and test subsets   
    return train_sets, val_sets, test_sets


# %%
# Training and Generating Predictions
# =====================================
#
# We create another :py:func:`~flytekit:flytekit.dynamic` workflow to train the model and generate predictions.
# Training and generating predictions ensue in parallel as a single task.
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def parallel_fit_predict(
    multi_train: typing.List[pd.DataFrame],
    multi_val: typing.List[pd.DataFrame],
    multi_test: typing.List[pd.DataFrame],
) -> typing.List[typing.List[float]]:
    preds = []
    
    # generate predictions for multiple regions
    for loc, train, val, test in zip(LOCATIONS, multi_train, multi_val, multi_test):
        model = fit(loc=loc, train=train, val=val)
        preds.append(predict(test=test, model_ser=model))

    return preds


# %%
# Lastly, we define a workflow to run the pipeline.
@workflow
def multi_region_house_price_prediction_model_trainer(
    seed: int = 7, number_of_houses: int = NUM_HOUSES_PER_LOCATION
) -> typing.List[typing.List[float]]:

    # generate and split the data
    split_data_vals = generate_and_split_data_multiloc(
        locations=LOCATIONS,
        number_of_houses_per_location=number_of_houses,
        seed=seed,
    )

    # fit the XGBoost model for multiple regions in parallel
    # generate predictions for multiple regions
    predictions = parallel_fit_predict(
        multi_train=split_data_vals.train_data,
        multi_val=split_data_vals.val_data,
        multi_test=split_data_vals.test_data,
    )

    return predictions


# %%
# Running the Model Locally
# ==========================
#
# We can run the workflow locally provided the required libraries are installed. The output would be a list of lists of house prices based on region, generated using the XGBoost model.
if __name__ == "__main__":
    print(multi_region_house_price_prediction_model_trainer())