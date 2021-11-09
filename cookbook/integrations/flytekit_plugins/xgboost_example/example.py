from dataclasses import asdict, dataclass
from typing import Dict, List, NamedTuple

import xgboost
from dataclasses_json import dataclass_json
from flytekitplugins.xgboost import TrainParameters, XGBoostTask

from flytekit import kwtypes, task, workflow
from flytekit.types.file import FlyteFile, JoblibSerializedFile


@dataclass_json
@dataclass
class Hyperparameters:
    max_depth: int = 2
    eta: int = 1
    objective: str = "binary:logistic"
    verbosity: int = 2


xgboost_trainer = XGBoostTask(
    name="xgboost_trainer",
    hyperparameters=asdict(Hyperparameters()),
    task_config=TrainParameters(num_boost_round=2),
    inputs=kwtypes(train=FlyteFile, test=FlyteFile, validation=FlyteFile),
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
        train=train, test=test, validation=validation
    )
    return (
        model,
        estimate_accuracy(predictions=predictions, test=test),
        evaluation_result,
    )


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running full_pipeline(), accuracy of the XGBoost model is {full_pipeline().accuracy:.2f}%"
    )
