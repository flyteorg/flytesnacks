from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import urllib.request as _request

import cv2
from flytekit.common import utils
from flytekit.sdk.tasks import python_task, outputs, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Output, Input


from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

# Since we are working with a specific dataset, we will create a strictly typed schema for the dataset.
# If we wanted a generic data splitter we could use a Generic schema without any column type and name information
# Example file: https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
# CSV Columns
#  1. Number of times pregnant
#  2. Plasma glucose concentration a 2 hours in an oral glucose tolerance test
#  3. Diastolic blood pressure (mm Hg)
#  4. Triceps skin fold thickness (mm)
#  5. 2-Hour serum insulin (mu U/ml)
#  6. Body mass index (weight in kg/(height in m)^2)
#  7. Diabetes pedigree function
#  8. Age (years)
#  9. Class variable (0 or 1)
# Example Row: 6,148,72,35,0,33.6,0.627,50,1
DATASET_SCHEMA = Types.Schema([
    ('#preg', Types.Integer),
    ('pgc_2h', Types.Integer),
    ('diastolic_bp', Types.Integer),
    ('tricep_skin_fold_mm', Types.Integer),
    ('serum_insulin_2h', Types.Integer),
    ('bmi', Types.Float),
    ('diabetes_pedigree', Types.Float),
    ('age', Types.Integer),
    ('class', Types.Integer),
])

# load data
# Example file: https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
@inputs(dataset_loc=Types.CSV, seed=Types.Integer, test_split_ratio=Types.Float)
@outputs(x_train=DATASET_SCHEMA, x_test=DATASET_SCHEMA, y_train=DATASET_SCHEMA, y_test=DATASET_SCHEMA)
@python_task(cache_version='1.0',cache=True)
def get_traintest_splitdatabase(ctx, dataset_loc, seed, test_split_ratio, x_train, x_test, y_train, y_test):
        dataset_loc.download()
        dataset = loadtxt(dataset_loc.local_path, delimiter=",") 
        # split data into X and y
        X = dataset[:,0:8]
        Y = dataset[:,8]

        # split data into train and test sets
        # seed = 7
        # test_size = 0.33
        _x_train,_ x_test, _y_train, _y_test = train_test_split(
                X, Y, test_size=test_split_ratio, random_state=seed)
        x_train.set(_x_train)
        x_test.set(_x_test)
        y_train.set(_y_train)
        y_test.set(_y_test)


@inputs(x_train=DATASET_SCHEMA, y_train=DATASET_SCHEMA)
@outputs(model=Types.Blob(format=".joblib.dat"))
@python_task(cache_version='1.0',cache=True)
def fit(ctx, x_train, y_train, model):
    # fit model no training data
    model = XGBClassifier()
    model.fit(X_train, y_train)
    fname = "model.joblib.dat"
    joblib.dump(model, fname)
    model.set(fname)


@inputs(x=DATASET_SCHEMA, model_ser=Types.Blob(format=".joblib.dat"))
@outputs(predictions=[Types.Integer])
@python_task(cache_version='1.0',cache=True)
def predict(ctx, model_ser, predictions):
    fname = "model.joblib.dat"
    model_ser.download(fname)
    model = joblib.load(fname)
    # make predictions for test data
    y_pred = model.predict(x)
    predictions.set([round(value) for value in y_pred])


@inputs(predictions=[Types.Integer], y_test=DATASET_SCHEMA)
@outputs(accuracy=Types.Float)
@python_task(cache_version='1.0',cache=True)
def score(ctx, predictions, y_test, accuracy):
    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    accuracy.set(accuracy)

    
@workflow_class
class DiabetesXGBoostModelTrainer(object):
    dataset = Input(
            Types.CSV(),
            default=Types.CSV.create_at_known_location("https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"),
            help="A CSV File that matches the format https://github.com/jbrownlee/Datasets/blob/master/pima-indians-diabetes.names",)

    test_split_ratio = Input(Types.Float, default=0.33, help="Ratio of how much should be test to Train")
    seed = Input(Types.Integer, default=7, help="What should be the seed used for splitting")

    split = get_traintest_splitdatabase(datase_loct=dataset, seed=seed, test_split_ratio=test_split_ratio)
    fit_task = fit(x_train=split.x_train, y_train=split.y_train)
    predicted = predict(model_ser=fit_task.outputs.model, x=split.outputs.x_test)
    score_task = score(predicted.outputs.predictions, y_test=split.outputs.y_test)

    model = Output(fit_task.outputs.model, sdk_type=Types.Blob)
    accuracy = Output(score_task.outputs.accuracy, sdk_type=Types.Float)
