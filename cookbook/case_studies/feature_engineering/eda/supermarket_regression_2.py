"""
Supermarket Regression 2 Notebook
=================================

"""

dataset = ""

import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

dataset = pd.DataFrame.from_dict(json.loads(dataset))
y_target = dataset["Product_Supermarket_Sales"]
dataset.drop(["Product_Supermarket_Sales"], axis=1, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(dataset, y_target, test_size=0.3)

print("Training data is", X_train.shape)
print("Training target is", y_train.shape)
print("test data is", X_test.shape)
print("test target is", y_test.shape)

from sklearn.preprocessing import RobustScaler, StandardScaler

scaler = RobustScaler()

scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

X_train[:5, :5]

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold, cross_val_score


def cross_validate(model, nfolds, feats, targets):
    score = -1 * (
        cross_val_score(
            model, feats, targets, cv=nfolds, scoring="neg_mean_absolute_error"
        )
    )
    return np.mean(score)


n_estimators = 150
max_depth = 3
max_features = "sqrt"
min_samples_split = 4
random_state = 2

from sklearn.ensemble import GradientBoostingRegressor

gb_model = GradientBoostingRegressor(
    n_estimators=n_estimators,
    max_depth=max_depth,
    max_features=max_features,
    min_samples_split=min_samples_split,
    random_state=random_state,
)

mae_score = cross_validate(gb_model, 10, X_train, y_train)
print("MAE Score: ", mae_score)

from flytekitplugins.papermill import record_outputs

record_outputs(mae_score=float(mae_score))
