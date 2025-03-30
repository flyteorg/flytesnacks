from typing import Dict, List, NamedTuple

import xgboost
from flytekitplugins.xgboost import (
    HyperParameters,
    ModelParameters,
    XGBoostParameters,
    XGBoostTrainerTask,
)

from flytekit import kwtypes, task, workflow
from flytekit.types.file import FlyteFile, JoblibSerializedFile


xgboost_trainer = XGBoostTrainerTask(
    name="xgboost_trainer",
    config=XGBoostParameters(
        hyper_parameters=HyperParameters(
            max_depth=2, eta=1, objective="binary:logistic", verbosity=2
        ),
    ),
    inputs=kwtypes(
        train=FlyteFile,
        test=FlyteFile,
        validation=FlyteFile,
        model_parameters=ModelParameters,
    ),
)


@task
def estimate_accuracy(predictions: List[float], test: FlyteFile) -> float:
    test.download()
    dtest = xgboost.DMatrix(test.path)
    labels = dtest.get_label()
    return (
        sum(
            1 for i in range(len(predictions)) if int(predictions[i] > 0.5) == labels[i]
        )
        / float(len(predictions))
        * 100.0
    )


wf_output = NamedTuple(
    "wf_output",
    model=JoblibSerializedFile,
    accuracy=float,
    evaluation_result=Dict[str, Dict[str, List[float]]],
)


@workflow
def full_pipeline(
    train: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train",
    test: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test",
    validation: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test",
) -> wf_output:
    model, predictions, evaluation_result = xgboost_trainer(
        train=train,
        test=test,
        validation=validation,
        model_parameters=ModelParameters(num_boost_round=2),
    )
    return (
        model,
        estimate_accuracy(
            predictions=predictions,
            test=test,
        ),
        evaluation_result,
    )


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running full_pipeline(), accuracy of the XGBoost model is {full_pipeline().accuracy:.2f}%"
    )
