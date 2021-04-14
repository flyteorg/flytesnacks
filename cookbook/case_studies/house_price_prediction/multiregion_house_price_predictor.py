"""
Predicting House Prices in Multiple Regions Using an XGBoost Model and Flytekit (Python)
----------------------------------------------------------------------------------------

"""

# %%
# Step 1: Importing the Libraries
# ----------------------------------
import typing

import flytekit
import pandas as pd
from flytekit import Resources, dynamic, task, workflow
from flytekit.types.file import FlyteFile

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
# Step 2: Initializing the Variables
# ----------------------------------
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
# Step 3: Task -- Generating & Splitting the Data for Multiple Regions
# --------------------------------------------------------------------
#
# Train, validation, and test datasets are lists of DataFrames.

dataset = typing.NamedTuple(
    "GenerateSplitDataOutputs",
    train_data=typing.List[pd.DataFrame],
    val_data=typing.List[pd.DataFrame],
    test_data=typing.List[pd.DataFrame],
)


@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def generate_and_split_data_multiloc(
    locations: typing.List[str],
    number_of_houses_per_location: int,
    seed: int,
) -> dataset:
    train_sets = []
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
    return train_sets, val_sets, test_sets


# %%
# Step 4: Dynamic Task -- Training the XGBoost Model & Generating the Predictionsfor Multiple Regions
# -----------------------------------------------------------------------
# (A "Dynamic" Task (aka Workflow) spins up internal workflows)
#
# Fit the model to the data and generate predictions (two functionalities in a single task to make it more powerful!)
# Note: You can also use two separate methods to fit the model and generate predictions but this basically means parallelizing an entire set of tasks.
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def parallel_fit_predict(
    multi_train: typing.List[pd.DataFrame],
    multi_val: typing.List[pd.DataFrame],
    multi_test: typing.List[pd.DataFrame],
) -> typing.List[typing.List[float]]:
    preds = []

    for loc, train, val, test in zip(LOCATIONS, multi_train, multi_val, multi_test):
        model = fit(loc=loc, train=train, val=val)
        preds.append(predict(test=test, model_ser=model))

    return preds


# %%
# Step 5: Workflow -- Defining the Workflow
# -----------------------------------------
#
# #. Generate and split the data
# #. Parallelly fit the XGBoost model for multiple regions
# #. Generate predictions for multiple regions
@workflow
def multi_region_house_price_prediction_model_trainer(
    seed: int = 7, number_of_houses: int = NUM_HOUSES_PER_LOCATION
) -> typing.List[typing.List[float]]:

    # Generate and split the data
    split_data_vals = generate_and_split_data_multiloc(
        locations=LOCATIONS,
        number_of_houses_per_location=number_of_houses,
        seed=seed,
    )

    # Parallelly fit the XGBoost model for multiple regions
    # Generate predictions for multiple regions
    predictions = parallel_fit_predict(
        multi_train=split_data_vals.train_data,
        multi_val=split_data_vals.val_data,
        multi_test=split_data_vals.test_data,
    )

    return predictions


# %%
# Trigger the workflow locally by calling the workflow function.
if __name__ == "__main__":
    print(multi_region_house_price_prediction_model_trainer())


# %%
# The output will be a list of lists (one list per region) of house price predictions.