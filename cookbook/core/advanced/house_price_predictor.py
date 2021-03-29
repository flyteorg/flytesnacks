##############################
# The example has been borrowed from Sagemaker examples
# https://github.com/awslabs/amazon-sagemaker-examples/blob/master/advanced_functionality/multi_model_xgboost_home_value/xgboost_multi_model_endpoint_home_value.ipynb
# Idea is to illustrate parallelized execution and eventually also show Sagemaker execution
###########################
## Libraries ##
# pip install sklearn
# pip install joblib
# pip install xgboost
# brew install libomp (Mac)
###########################

import os
import typing

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from flytekit import Resources, dynamic, task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory


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

MAX_YEAR = 2021
SPLIT_RATIOS = [0.6, 0.3, 0.1]


def gen_price(house) -> int:
    _base_price = int(house["SQUARE_FEET"] * 150)
    _price = int(
        _base_price
        + (10000 * house["NUM_BEDROOMS"])
        + (15000 * house["NUM_BATHROOMS"])
        + (15000 * house["LOT_ACRES"])
        + (15000 * house["GARAGE_SPACES"])
        - (5000 * (MAX_YEAR - house["YEAR_BUILT"]))
    )
    return _price


def gen_random_house() -> typing.List:
    _house = {
        "SQUARE_FEET": int(np.random.normal(3000, 750)),
        "NUM_BEDROOMS": np.random.randint(2, 7),
        "NUM_BATHROOMS": np.random.randint(2, 7) / 2,
        "LOT_ACRES": round(np.random.normal(1.0, 0.25), 2),
        "GARAGE_SPACES": np.random.randint(0, 4),
        "YEAR_BUILT": min(MAX_YEAR, int(np.random.normal(1995, 10))),
    }
    _price = gen_price(_house)
    return [
        _price,
        _house["YEAR_BUILT"],
        _house["SQUARE_FEET"],
        _house["NUM_BEDROOMS"],
        _house["NUM_BATHROOMS"],
        _house["LOT_ACRES"],
        _house["GARAGE_SPACES"],
    ]


def gen_houses(num_houses) -> pd.DataFrame:
    _house_list = []
    for i in range(num_houses):
        _house_list.append(gen_random_house())
    _df = pd.DataFrame(
        _house_list,
        columns=[
            "PRICE",
            "YEAR_BUILT",
            "SQUARE_FEET",
            "NUM_BEDROOMS",
            "NUM_BATHROOMS",
            "LOT_ACRES",
            "GARAGE_SPACES",
        ],
    )
    return _df


def split_data(
    df: pd.DataFrame, seed: int, split: typing.List[float]
) -> (np.ndarray, np.ndarray, np.ndarray):
    # split data into train and test sets
    seed = seed
    val_size = split[1]
    test_size = split[2]

    num_samples = df.shape[0]
    x1 = df.values[
        :num_samples, 1:
    ]  # keep only the features, skip the target, all rows
    y1 = df.values[:num_samples, :1]  # keep only the target, all rows

    # Use split ratios to divide up into train/val/test
    x_train, x_val, y_train, y_val = train_test_split(
        x1, y1, test_size=(test_size + val_size), random_state=seed
    )
    # Of the remaining non-training samples, give proper ratio to validation and to test
    x_test, x_test, y_test, y_test = train_test_split(
        x_val, y_val, test_size=(test_size / (test_size + val_size)), random_state=seed
    )
    # Reassemble the datasets with target in first column and features after that
    _train = np.concatenate([y_train, x_train], axis=1)
    _val = np.concatenate([y_val, x_val], axis=1)
    _test = np.concatenate([y_test, x_test], axis=1)

    return _train, _val, _test


def generate_data(
    loc: str, number_of_houses: int, seed: int
) -> (np.ndarray, np.ndarray, np.ndarray):
    _houses = gen_houses(number_of_houses)
    _train, _val, _test = split_data(_houses, seed, split=SPLIT_RATIOS)
    return _train, _val, _test


def save_to_dir(path: str, n: str, arr: np.ndarray) -> str:
    d = os.path.join(path, n)
    os.makedirs(d, exist_ok=True)
    save_to_file(d, n, arr)
    return d


def save_to_file(path: str, n: str, arr: np.ndarray) -> str:
    f = f"{n}.csv"
    f = os.path.join(path, f)
    np.savetxt(f, arr, delimiter=",", fmt="%.2f")
    return f


# Generating and Splitting the Data
@task(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def generate_and_split_data(
    loc: str, number_of_houses: int, seed: int
) -> (
    FlyteDirectory[typing.TypeVar("csv")],
    FlyteDirectory[typing.TypeVar("csv")],
    FlyteFile[typing.TypeVar("csv")],
):
    _train, _val, _test = generate_data(loc, number_of_houses, seed)
    os.makedirs("data", exist_ok=True)
    train = save_to_dir("data", "train", _train)
    val = save_to_dir("data", "val", _val)
    test = save_to_file("data", "test", _test)
    return train, val, test


# Training the XGBoost Model
@task(cache_version="1.0", cache=True, limits=Resources(mem="600Mi"))
def fit(
    loc: str,
    train: FlyteDirectory[typing.TypeVar("csv")],
) -> FlyteFile[typing.TypeVar("joblib.dat")]:
    """
    This function takes the given input features and their corresponding classes to train a XGBClassifier.
    NOTE: We have simplified the algorithm for demo. Default hyper params & no validation dataset :P.
    """
    files = os.listdir(train)

    # We know we are writing just one file, so we will just read the one file
    df = pd.read_csv(os.path.join(train, files[0]), header=None)
    y = df[df.columns[0]]
    x = df[df.columns[1:]]

    # Fit model no training data
    m = XGBClassifier()
    m.fit(x, y)

    fname = "model-" + loc + ".joblib.dat"
    joblib.dump(m, fname)
    return fname


# Generating the Predictions
@task(cache_version="1.0", cache=True, limits=Resources(mem="600Mi"))
def predict(
    test: FlyteFile[typing.TypeVar("csv")],
    model_ser: FlyteFile[typing.TypeVar("joblib.dat")],
) -> typing.List[float]:
    """
    Given a any trained model, serialized using joblib (this method can be shared!) and features, this method returns
    predictions.
    """
    # Load model
    model = joblib.load(model_ser)

    # Load test data
    test_df = pd.read_csv(test, header=None)
    x_df = test_df[test_df.columns[1:]]

    y_pred = model.predict(x_df).tolist()

    return y_pred


@workflow
def house_price_predictor_trainer():
    """
    This pipeline trains an XGBoost model, also generated synthetic data and runs predictions against test dataset
    """

    train, _, test = generate_and_split_data(
        loc=LOCATIONS[0], number_of_houses=NUM_HOUSES_PER_LOCATION, seed=7
    )
    fit_task = fit(loc=LOCATIONS[0], train=train)
    predictions = predict(model_ser=fit_task, test=test)

    print(predictions)