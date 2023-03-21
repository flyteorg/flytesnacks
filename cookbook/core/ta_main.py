import typing
from dataclasses import dataclass

import numpy as np
from dataclasses_json import dataclass_json
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


@dataclass_json
@dataclass
class Hyperparameters(object):
    n_samples: int = 1000
    n_features: int = 20
    n_informative: int = 15
    n_classes: int = 2
    test_size: float = 0.2
    n_estimator: int = 100


# Generate the dataset
def generate_dataset(hp: Hyperparameters) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X, y = make_classification(n_samples=hp.n_samples, n_features=hp.n_features, n_informative=hp.n_informative,
                               n_classes=hp.n_classes)
    return train_test_split(X, y, test_size=hp.test_size)


# Train a random forest classifier on the train data
def train_model(hp: Hyperparameters, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    return RandomForestClassifier(hp.n_estimator).fit(X_train, y_train)
