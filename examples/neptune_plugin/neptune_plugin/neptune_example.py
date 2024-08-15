# %% [markdown]
# (neptune_example)=
#
# # Neptune Example
# Neptune is the MLOps stack component for experiment tracking. It offers a single place
# to log, compare, store, and collaborate on experiments and models. This plugin
# enables seamless use of Neptune within Flyte by configuring links between the
# two platforms. In this example, we learn how to train scale up training multiple
# XGBoost models and use Neptune for tracking.
# %%
from typing import List, Tuple

import numpy as np
from flytekit import (
    ImageSpec,
    Resources,
    Secret,
    current_context,
    dynamic,
    task,
    workflow,
)
from flytekitplugins.neptune import neptune_init_run

# %% [markdown]
# First, we specify the neptune project that we will use with Neptune
# Please update `NEPTUNE_PROJECT` to the value associated with your account.
WANDB_PROJECT = "username/project"

# %% [markdown]
# W&B requires an API key to authenticate with their service. In the above example,
# the secret is created using
# [Flyte's Secrets manager](https://docs.flyte.org/en/latest/user_guide/productionizing/secrets.html).
api_key = Secret(key="neptune-api-token", group="neptune-api-group")

# %% [mardkwon]
# Next, we use `ImageSpec` to construct a container with the dependencies for our
# XGBoost training task. Please set the `REGISTRY` to an registry that your cluster can access;
REGISTRY = "localhost:30000"

image = ImageSpec(
    name="flytekit-xgboost",
    apt_packages=["git"],
    packages=[
        "neptune",
        "neptune-xgboost",
        "flytekitplugins-neptune",
        "scikit-learn==1.5.1",
        "numpy==1.26.1",
        "matplotlib==3.9.2",
    ],
    builder="default",
    registry=REGISTRY,
)


# %%
# First, we use a task to download the dataset and cache the data in Flyte:
@task(
    container_image=image,
    cache=True,
    cache_version="v2",
    requests=Resources(cpu="2", mem="2Gi"),
)
def get_dataset() -> Tuple[np.ndarray, np.ndarray]:
    from sklearn.datasets import fetch_california_housing

    X, y = fetch_california_housing(return_X_y=True, as_frame=False)
    return X, y


# %%
# Next, we use the `neptune_init_run` decorator to configure Flyte to train an XGBoost
# model. The decorator requires an `api_key` secret to authenticate with Neptune and
# the task definition needs to requests the same `api_key` secret. In the training
# function, the [Neptune run object](https://docs.neptune.ai/api/run/) is accessible
# through `current_context().neptune_run`, which is frequently used
# in Neptune's integrations. In this example, we pass the `Run` object into Neptune's
# XGBoost callback.
@task(
    container_image=image,
    secret_requests=[api_key],
    requests=Resources(cpu="2", mem="4Gi"),
)
@neptune_init_run(project=WANDB_PROJECT, secret=api_key)
def train_model(max_depth: int, X: np.ndarray, y: np.ndarray):
    import xgboost as xgb
    from neptune.integrations.xgboost import NeptuneCallback
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_test, label=y_test)

    ctx = current_context()
    run = ctx.neptune_run
    neptune_callback = NeptuneCallback(run=run)

    model_params = {
        "tree_method": "hist",
        "eta": 0.7,
        "gamma": 0.001,
        "max_depth": max_depth,
        "objective": "reg:squarederror",
        "eval_metric": ["mae", "rmse"],
    }
    evals = [(dtrain, "train"), (dval, "valid")]

    # Train the model and log metadata to the run in Neptune
    xgb.train(
        params=model_params,
        dtrain=dtrain,
        num_boost_round=57,
        evals=evals,
        callbacks=[
            neptune_callback,
            xgb.callback.LearningRateScheduler(lambda epoch: 0.99**epoch),
            xgb.callback.EarlyStopping(rounds=30),
        ],
    )


# %%
# With Flyte's dynamic workflows, we scale up multiple training jobs with different
# `max_depths`:
@dynamic(container_image=image)
def train_multiple_models(max_depths: List[int], X: np.ndarray, y: np.ndarray):
    for max_depth in max_depths:
        train_model(max_depth=max_depth, X=X, y=y)


@workflow
def train_wf(max_depths: List[int] = [2, 4, 10]):
    X, y = get_dataset()
    train_multiple_models(max_depths=max_depths, X=X, y=y)


# %%
# To run this workflow on a remote Flyte cluster run:
# ```bash
# union run --remote neptune_example.py train_wf
# ```


# %% [markdown]
# To enable dynamic log links, add plugin to Flyte's configuration file:
# ```yaml
# plugins:
#   logs:
#     dynamic-log-links:
#       - neptune-run-id:
#           displayName: Neptune
#           templateUris: "{{ .taskConfig.host }}/{{ .taskConfig.project }}?query=(%60Flyte%20Execution%20ID%60%3Astring%20%3D%20%22{{ .executionName }}-{{ .nodeId }}-{{ .taskRetryAttempt }}%22)&lbViewUnpacked=true"
# ```
