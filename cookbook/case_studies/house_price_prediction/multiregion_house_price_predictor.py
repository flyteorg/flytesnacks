# Step 1: Importing the Libraries
import typing

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

# Step 2: Initializing the Variables
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


# Step 3: Task -- Generating & Splitting the Data for Multiple Regions
# Train, validation, and test datasets are lists of DataFrames.
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def generate_and_split_data_multiloc(
    locations: typing.List[str],
    number_of_houses_per_location: int,
    seed: int,
) -> (typing.List[pd.DataFrame], typing.List[pd.DataFrame], typing.List[pd.DataFrame]):
    train_sets = []
    val_sets = []
    test_sets = []
    for loc in locations:
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


# Step 4: Dynamic Task -- Training the XGBoost Model for Multiple Regions
# (A "Dynamic" Task (aka Workflow) spins up internal workflows)
# Serialize the XGBoost models using joblib and store the models in dat files.
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def parallel_fit(
    multi_train: typing.List[pd.DataFrame], multi_val: typing.List[pd.DataFrame]
) -> typing.List[FlyteFile[typing.TypeVar("joblib.dat")]]:
    models = []
    for loc, train, val in zip(LOCATIONS, multi_train, multi_val):
        t = fit(loc=loc, train=train, val=val)
        models.append(t)
    return models


# Step 5: Dynamic Task -- Generating the Predictions for Multiple Regions
# (A "Dynamic" Task (aka Workflow) spins up internal workflows)
# Unserialize the XGBoost models using joblib and generate the predictions.
@dynamic(cache_version="1.1", cache=True, limits=Resources(mem="600Mi"))
def parallel_predict(
    multi_test: typing.List[pd.DataFrame],
    multi_models: typing.List[FlyteFile[typing.TypeVar("joblib.dat")]],
) -> typing.List[typing.List[float]]:
    preds = []

    for test, model in zip(multi_test, multi_models):
        p = predict(test=test, model_ser=model)
        preds.append(p)

    return preds


@task
def diffs(
    original_test_data: typing.List[pd.DataFrame],
    predictions: typing.List[typing.List[float]],
) -> typing.List[typing.List[float]]:
    offs = []
    for orig_test_data, pred in zip(original_test_data, predictions):
        offs.append(pred - orig_test_data["PRICE"])
    return offs


# Step 6: Workflow -- Defining the Workflow
# #. Generate and split the data
# #. Parallelly fit the XGBoost model for multiple regions
# #. Generate predictions for multiple regions
@workflow
def multi_region_house_price_prediction_model_trainer(
    seed: int = 7, number_of_houses: int = NUM_HOUSES_PER_LOCATION
) -> (typing.List[typing.List[float]], typing.List[typing.List[float]]):
    # Generate and split the data
    train, val, test = generate_and_split_data_multiloc(
        locations=LOCATIONS,
        number_of_houses_per_location=number_of_houses,
        seed=seed,
    )

    # Parallelly fit the XGBoost model for multiple regions
    model = parallel_fit(multi_train=train, multi_val=val)

    # Generate predictions for multiple regions
    predictions = parallel_predict(multi_models=model, multi_test=test)
    off = diffs(original_test_data=test, predictions=predictions)

    return predictions, off


# Trigger the workflow locally by calling the workflow function.
# The output will be a list of lists (one list per region) of house price predictions.
if __name__ == "__main__":
    print(multi_region_house_price_prediction_model_trainer())


