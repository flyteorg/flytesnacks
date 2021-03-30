"""
Predicting House Prices in Multiple Regions Using an XGBoost Model and Flytekit (Python)
----------------------------------------------------------------------------------------

"""

# %%
# Step 1: Importing the Libraries
# ----------------------------------
import os
import typing

import flytekit
from flytekit import Resources, dynamic, task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory

try:
    from .house_price_predictor import (
        generate_data,
        save_to_file,
        save_to_dir,
        fit,
        predict,
    )
except ImportError:
    from house_price_predictor import (
        generate_data,
        save_to_file,
        save_to_dir,
        fit,
        predict,
    )

# %%
# Step 2: Initializing the Variables
# ----------------------------------
NUM_HOUSES_PER_LOCATION = 1000
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
# Train and validation datasets are a list of directories (consisting of one CSV file per directory) and test data is a list of CSV files
@task(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def generate_and_split_data_multiloc(
    locations: typing.List[str],
    number_of_houses_per_location: int,
    seed: int,
) -> (
    typing.List[FlyteDirectory[typing.TypeVar("csv")]],
    typing.List[FlyteDirectory[typing.TypeVar("csv")]],
    typing.List[FlyteFile[typing.TypeVar("csv")]],
):
    train_sets = []
    val_sets = []
    test_sets = []
    for loc in locations:
        _train, _val, _test = generate_data(loc, number_of_houses_per_location, seed)
        dir = "multi_data"
        os.makedirs(dir, exist_ok=True)
        train_sets.append(save_to_dir(os.path.join(dir, loc), "train", _train))
        val_sets.append(save_to_dir(os.path.join(dir, loc), "val", _val))
        test_sets.append(save_to_file(os.path.join(dir, loc), "test", _test))
    return train_sets, val_sets, test_sets

# %%
# Step 4: Dynamic Task -- Training the XGBoost Model for Multiple Regions
# -----------------------------------------------------------------------
# (A "Dynamic" Task (aka Workflow) spins up internal workflows)
#
# Serialize the XGBoost models using joblib and store the models in dat files
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def parallel_fit(
    multi_train: typing.List[FlyteDirectory[typing.TypeVar("csv")]],
) -> typing.List[FlyteFile[typing.TypeVar("joblib.dat")]]:
    models = []
    for loc, train in zip(LOCATIONS, multi_train):
        t = fit(
            loc=loc,
            train=train,
        )
        models.append(t)
    return models

# %%
# Step 5: Dynamic Task -- Generating the Predictions for Multiple Regions 
# -----------------------------------------------------------------------
# (A "Dynamic" Task (aka Workflow) spins up internal workflows)
#
# Unserialize the XGBoost models using joblib and generate the predictions
@dynamic(cache_version="1.1", cache=True, limits=Resources(mem="600Mi"))
def parallel_predict(
    multi_test: typing.List[FlyteFile[typing.TypeVar("csv")]],
    multi_models: typing.List[FlyteFile[typing.TypeVar("joblib.dat")]],
) -> typing.List[typing.List[float]]:
    preds = []

    for test, model in zip(multi_test, multi_models):
        p = predict(test=test, model_ser=model)
        preds.append(p)

    return preds

# %%
# Step 6: Workflow -- Defining the Workflow
# -----------------------------------------
# #. Generate and split the data
# #. Parallelly fit the XGBoost model for multiple regions
# #. Generate predictions for multiple regions
@workflow
def multi_region_house_price_prediction_model_trainer():

    """
    This pipeline trains an XGBoost model, also generated synthetic data and runs predictions against test dataset
    """

    train, _, test = generate_and_split_data_multiloc(
        locations=LOCATIONS,
        number_of_houses_per_location=NUM_HOUSES_PER_LOCATION,
        seed=7,
    )
    fit_task = parallel_fit(multi_train=train)
    predictions = parallel_predict(multi_models=fit_task, multi_test=test)

    return predictions

# %%
# Trigger the workflow locally by calling the workflow function
if __name__ == "__main__":
    print(multi_region_house_price_prediction_model_trainer())

# %%
# The output will be a list of lists (one list per region) of house prices predictions.