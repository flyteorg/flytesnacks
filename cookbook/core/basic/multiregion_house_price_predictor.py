import os
import typing

from flytekit import Resources, dynamic, task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory

from .house_price_predictor import (
    generate_data,
    save_to_file,
    save_to_dir,
    fit,
    predict,
)


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

# Generating and Splitting the Data for Multiple Regions
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


# Training the XGBoost Model for Multiple Regions
# A "Dynamic" Task (aka Workflow) spins up internal workflows
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


# Generating the Predictions
# A "Dynamic" Task (aka Workflow) spins up internal workflows
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

    print(predictions)


if __name__ == "__main__":
    multi_region_house_price_prediction_model_trainer()
