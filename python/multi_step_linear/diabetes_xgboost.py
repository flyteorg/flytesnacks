from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import joblib
import pandas as pd
from flytekit.sdk.tasks import python_task, outputs, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Output, Input
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

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
TYPED_COLUMNS = [
    ('#preg', Types.Integer),
    ('pgc_2h', Types.Integer),
    ('diastolic_bp', Types.Integer),
    ('tricep_skin_fold_mm', Types.Integer),
    ('serum_insulin_2h', Types.Integer),
    ('bmi', Types.Float),
    ('diabetes_pedigree', Types.Float),
    ('age', Types.Integer),
    ('class', Types.Integer),
]
DATASET_SCHEMA = Types.Schema(TYPED_COLUMNS)
FEATURES_SCHEMA = Types.Schema(TYPED_COLUMNS[:8])
CLASSES_SCHEMA = Types.Schema([TYPED_COLUMNS[-1]])


# load data
# Example file: https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
@inputs(dataset=Types.CSV, seed=Types.Integer, test_split_ratio=Types.Float)
@outputs(x_train=FEATURES_SCHEMA, x_test=FEATURES_SCHEMA, y_train=CLASSES_SCHEMA, y_test=CLASSES_SCHEMA)
@python_task(cache_version='1.0', cache=True)
def get_traintest_splitdatabase(ctx, dataset, seed, test_split_ratio, x_train, x_test, y_train, y_test):
    dataset.download()
    column_names = [k for k in DATASET_SCHEMA.columns.keys()]
    df = pd.read_csv(dataset.local_path, names=column_names)

    # Select all features
    x = df[column_names[:8]]
    # Select only the classes
    y = df[[column_names[-1]]]

    # split data into train and test sets
    _x_train, _x_test, _y_train, _y_test = train_test_split(
        x, y, test_size=test_split_ratio, random_state=seed)

    def pd_df_to_schema(_schema, _df):
        arr_schema = _schema()
        with arr_schema as w:
            w.write(_df)
        return arr_schema

    # https: // github.com / lyft / flytekit / blob / master / flytekit / common / types / impl / schema.py  # L592
    # Add support for pd, directly
    x_train.set(pd_df_to_schema(FEATURES_SCHEMA, _x_train))
    x_test.set(pd_df_to_schema(FEATURES_SCHEMA, _x_test))
    y_train.set(pd_df_to_schema(CLASSES_SCHEMA, _y_train))
    y_test.set(pd_df_to_schema(CLASSES_SCHEMA, _y_test))


@inputs(x=FEATURES_SCHEMA, y=CLASSES_SCHEMA)
@outputs(model=Types.Blob)  # TODO: Support for subtype format=".joblib.dat"))
@python_task(cache_version='1.0', cache=True)
def fit(ctx, x, y, model):
    with x as r:
        x_df = r.read()
    with y as r:
        y_df = r.read()
    # fit model no training data
    m = XGBClassifier()
    m.fit(x_df, y_df)
    fname = "model.joblib.dat"
    joblib.dump(m, fname)
    model.set(fname)


@inputs(x=FEATURES_SCHEMA, model_ser=Types.Blob)  # TODO: format=".joblib.dat"))
@outputs(predictions=[Types.Integer])
@python_task(cache_version='1.0', cache=True)
def predict(ctx, x, model_ser, predictions):
    fname = "model.joblib.dat"
    model_ser.download(fname)
    model = joblib.load(fname)
    # make predictions for test data
    with x as r:
        x_df = r.read()
    y_pred = model.predict(x_df)
    predictions.set([round(value) for value in y_pred])


@inputs(predictions=[Types.Integer], y_test=DATASET_SCHEMA)
@outputs(accuracy=Types.Float)
@python_task(cache_version='1.0', cache=True)
def score(ctx, predictions, y_test, accuracy):
    # evaluate predictions
    acc = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (acc * 100.0))
    accuracy.set(acc)


@workflow_class
class DiabetesXGBoostModelTrainer(object):
    dataset = Input(Types.CSV, default=Types.CSV.create_at_known_location(
        "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"),
                    help="A CSV File that matches the format https://github.com/jbrownlee/Datasets/blob/master/pima-indians-diabetes.names")

    test_split_ratio = Input(Types.Float, default=0.33, help="Ratio of how much should be test to Train")
    seed = Input(Types.Integer, default=7, help="What should be the seed used for splitting")

    split = get_traintest_splitdatabase(dataset=dataset, seed=seed, test_split_ratio=test_split_ratio)
    fit_task = fit(x=split.outputs.x_train, y=split.outputs.y_train)
    predicted = predict(model_ser=fit_task.outputs.model, x=split.outputs.x_test)
    score_task = score(predictions=predicted.outputs.predictions, y_test=split.outputs.y_test)

    model = Output(fit_task.outputs.model, sdk_type=Types.Blob)
    accuracy = Output(score_task.outputs.accuracy, sdk_type=Types.Float)
