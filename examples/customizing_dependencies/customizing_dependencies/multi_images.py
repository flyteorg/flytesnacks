# Multiple container images in a single workflow
import numpy as np
from flytekit import task, workflow


@task(container_image="{{.image.mindmeld.fqn}}:{{.image.mindmeld.version}}")
def get_data() -> np.ndarray:
    # here we're importing scikit learn within the Flyte task
    from sklearn import datasets

    iris = datasets.load_iris()
    X = iris.data[:, :2]
    return X


@task(container_image="{{.image.borebuster.fqn}}:{{.image.borebuster.version}}")
def normalize(X: np.ndarray) -> np.ndarray:
    return (X - X.mean(axis=0)) / X.std(axis=0)


@workflow
def multi_images_wf() -> np.ndarray:
    X = get_data()
    X = normalize(X=X)
    return X
