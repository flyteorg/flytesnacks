from flytekit.sdk.test_utils import flyte_test
from flytekit.sdk.types import Types

from multi_step_linear import diabetes_xgboost as dxgb


@flyte_test
def test_get_traintest_splitdatabase():
    dataset = Types.CSV.create_at_known_location(
        "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv")
    result = dxgb.get_traintest_splitdatabase.unit_test(dataset=dataset, seed=7, test_split_ratio=0.33)
    print(result.x_train)
