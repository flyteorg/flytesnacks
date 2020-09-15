##############################
# The example has been borrowed from Sagemaker examples
# https://github.com/awslabs/amazon-sagemaker-examples/blob/master/advanced_functionality/multi_model_xgboost_home_value/xgboost_multi_model_endpoint_home_value.ipynb
# Idea is to illustrate parallelized execution and eventually also show Sagemaker execution

import typing

import numpy as np
import pandas as pd
from flytekit.sdk.tasks import python_task, inputs, outputs
from flytekit.sdk.types import Types
from sklearn.model_selection import train_test_split

NUM_HOUSES_PER_LOCATION = 1000
LOCATIONS = ['NewYork_NY', 'LosAngeles_CA', 'Chicago_IL', 'Houston_TX', 'Dallas_TX',
             'Phoenix_AZ', 'Philadelphia_PA', 'SanAntonio_TX', 'SanDiego_CA', 'SanFrancisco_CA']

PARALLEL_TRAINING_JOBS = 4  # len(LOCATIONS) if your account limits can handle it
MAX_YEAR = 2019
SPLIT_RATIOS = [0.6, 0.3, 0.1]


def gen_price(house) -> int:
    _base_price = int(house['SQUARE_FEET'] * 150)
    _price = int(_base_price + (10000 * house['NUM_BEDROOMS']) + \
                 (15000 * house['NUM_BATHROOMS']) + \
                 (15000 * house['LOT_ACRES']) + \
                 (15000 * house['GARAGE_SPACES']) - \
                 (5000 * (MAX_YEAR - house['YEAR_BUILT'])))
    return _price


def gen_random_house() -> typing.List:
    _house = {'SQUARE_FEET': int(np.random.normal(3000, 750)),
              'NUM_BEDROOMS': np.random.randint(2, 7),
              'NUM_BATHROOMS': np.random.randint(2, 7) / 2,
              'LOT_ACRES': round(np.random.normal(1.0, 0.25), 2),
              'GARAGE_SPACES': np.random.randint(0, 4),
              'YEAR_BUILT': min(MAX_YEAR, int(np.random.normal(1995, 10)))}
    _price = gen_price(_house)
    return [_price, _house['YEAR_BUILT'], _house['SQUARE_FEET'],
            _house['NUM_BEDROOMS'], _house['NUM_BATHROOMS'],
            _house['LOT_ACRES'], _house['GARAGE_SPACES']]


def gen_houses(num_houses) -> pd.DataFrame:
    _house_list = []
    for i in range(num_houses):
        _house_list.append(gen_random_house())
    _df = pd.DataFrame(_house_list,
                       columns=['PRICE', 'YEAR_BUILT', 'SQUARE_FEET', 'NUM_BEDROOMS',
                                'NUM_BATHROOMS', 'LOT_ACRES', 'GARAGE_SPACES'])
    return _df


def split_data(df: pd.DataFrame, seed: int, split: typing.List[float]) -> (np.ndarray, np.ndarray, np.ndarray):
    # split data into train and test sets
    seed = seed
    val_size = split[1]
    test_size = split[2]

    num_samples = df.shape[0]
    x1 = df.values[:num_samples, 1:]  # keep only the features, skip the target, all rows
    y1 = df.values[:num_samples, :1]  # keep only the target, all rows

    # Use split ratios to divide up into train/val/test
    x_train, x_val, y_train, y_val = train_test_split(x1, y1, test_size=(test_size + val_size), random_state=seed)
    # Of the remaining non-training samples, give proper ratio to validation and to test
    x_test, x_test, y_test, y_test = train_test_split(x_val, y_val,
                                                      test_size=(test_size / (test_size + val_size)),
                                                      random_state=seed)
    # reassemble the datasets with target in first column and features after that
    _train = np.concatenate([y_train, x_train], axis=1)
    _val = np.concatenate([y_val, x_val], axis=1)
    _test = np.concatenate([y_test, x_test], axis=1)

    return _train, _val, _test


def generate_data(loc: str, number_of_houses: int, seed: int) -> typing.List[str]:
    _houses = gen_houses(number_of_houses)
    _train, _val, _test = split_data(_houses, seed, split=SPLIT_RATIOS)

    l = []
    f = f'{loc}_train.csv'
    np.savetxt(f, _train, delimiter=',', fmt='%.2f')
    l.append(f)
    f = f'{loc}_val.csv'
    np.savetxt(f, _val, delimiter=',', fmt='%.2f')
    l.append(f)
    f = f'{loc}_test.csv'
    np.savetxt(f, _test, delimiter=',', fmt='%.2f')
    l.append(f)

    return l


@inputs(loc=Types.String, number_of_houses=Types.Integer, seed=Types.Integer)
@outputs(data=[Types.CSV])
@python_task(cache=True, cache_version="0.1", cpu_request="1000Mi", memory_request="1Gi")
def generate_and_split_data(wf_params, loc, number_of_houses, seed, data):
    files = generate_data(loc, number_of_houses, seed)
    csvs = []
    for f in files:
        c = Types.CSV()
        c.set(f)
        csvs.append(c)
    data.set(csvs)


@inputs(locations=[Types.String], number_of_houses_per_location=Types.Integer, seed=Types.Integer)
@outputs(data=[Types.CSV])
@python_task(cache=True, cache_version="0.1", cpu_request="1000Mi", memory_request="1Gi")
def generate_and_split_data_multiloc(wf_params, locations, number_of_houses_per_location, seed, data):
    for loc in locations:
        generate_data(loc, number_of_houses_per_location, seed)
