from flytekit.sdk.test_utils import flyte_test
from flytekit.sdk.types import Types

from multi_step_linear import diabetes_xgboost as dxgb


@flyte_test
def test_DiabetesXGBoostModelTrainer():

    dataset = Types.CSV.create_at_known_location(
        "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv")

    # Test get dataset
    result = dxgb.get_traintest_splitdatabase.unit_test(dataset=dataset, seed=7, test_split_ratio=0.33)
    assert "x_train" in result
    assert "y_train" in result
    assert "x_test" in result
    assert "y_test" in result

    # Test fit
    m = dxgb.fit.unit_test(x=result["x_train"], y=result["y_train"])

    assert "model" in m

    p = dxgb.predict.unit_test(x=result["x_test"], model_ser=m["model"])
    assert "predictions" in p

    print(p)
