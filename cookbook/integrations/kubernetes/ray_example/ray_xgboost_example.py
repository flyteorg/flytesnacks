import numpy
import xgboost_ray
from flytekit import Resources, task, workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.ray import HeadNodeConfig, RayJobConfig, WorkerNodeConfig
from xgboost_ray import RayDMatrix, RayParams, train, predict
from sklearn.datasets import load_breast_cancer
import xgboost as xgb
# Refer to https://docs.ray.io/en/latest/ray-more-libs/xgboost-ray.html#usage


@task
def load_data() -> xgboost_ray.matrix.RayDMatrix:
    train_x, train_y = load_breast_cancer(return_X_y=True)
    train_set = RayDMatrix(train_x, train_y)
    return train_set


@task(task_config=RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "True"}),
    worker_node_config=[WorkerNodeConfig(group_name="ray-group", replicas=2)],
), limits=Resources(mem="2000Mi", cpu="1"))
def train_model(train_set: xgboost_ray.matrix.RayDMatrix) -> FlyteFile:
    evals_result = {}
    bst = train(
        {
            "objective": "binary:logistic",
            "eval_metric": ["logloss", "error"],
        },
        train_set,
        evals_result=evals_result,
        evals=[(train_set, "train")],
        verbose_eval=False,
        ray_params=RayParams(
            num_actors=2,  # Number of remote actors
            cpus_per_actor=1))

    model_path = "model.xgb"
    bst.save_model(model_path)
    print("Final training error: {:.4f}".format(evals_result["train"]["error"][-1]))
    return FlyteFile(model_path)


@task(limits=Resources(mem="2000Mi", cpu="1"))
def predict_data(model: FlyteFile, data: xgboost_ray.matrix.RayDMatrix) -> numpy.ndarray:
    bst = xgb.Booster(model_file=model.download())
    pred_ray = predict(bst, data, ray_params=RayParams(num_actors=2))
    return pred_ray


@workflow
def ray_workflow() -> numpy.ndarray:
    data = load_data()
    model = train_model(train_set=data)
    return predict_data(model=model, data=data)


if __name__ == "__main__":
    print(ray_workflow())

