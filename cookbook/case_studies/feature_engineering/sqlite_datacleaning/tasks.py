import numpy as np
import pandas as pd
from flytekit import task
from numpy.core.fromnumeric import sort
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer


@task
def mean_median_imputer(
    dataframe: pd.DataFrame,
    imputation_method: str,
) -> pd.DataFrame:

    dataframe = dataframe.replace("?", np.nan)
    if imputation_method not in ["median", "mean"]:
        raise ValueError("imputation_method takes only values 'median' or 'mean'")

    imputer = SimpleImputer(missing_values=np.nan, strategy=imputation_method)

    imputer = imputer.fit(dataframe)
    dataframe[:] = imputer.transform(dataframe)

    return dataframe


@task
def univariate_selection(
    dataframe: pd.DataFrame, split_mask: int, num_features: int
) -> pd.DataFrame:

    X = dataframe.iloc[:, 0:split_mask]
    y = dataframe.iloc[:, split_mask]
    test = SelectKBest(score_func=f_classif, k=num_features)
    fit = test.fit(X, y)
    indices = sort((-fit.scores_).argsort()[:num_features])
    column_names = map(dataframe.columns.__getitem__, indices)
    features = fit.transform(X)
    return pd.DataFrame(features, columns=column_names)
