# %% [markdown]
# (wandb_example)=
#
# # Weights and Biases Example
# The Weights & Biases MLOps platform helps AI developers streamline their ML
# workflow from end-to-end. This plugin enables seamless use of Weights & Biases
# within Flyte by configuring links between the two platforms.
# %%
from flytekit import ImageSpec, Secret, task, workflow
from flytekitplugins.wandb import wandb_init

# %% [markdown]
# First, we specify the project and entity that we will use with Weights and Biases.
# Please update `WANDB_ENTITY` to the value associated with your account.
# %%
WANDB_PROJECT = "flytekit-wandb-plugin"
WANDB_ENTITY = "github-username"

# %% [markdown]
# W&B requires an API key to authenticate with their service. In the above example,
# the secret is created using
# [Flyte's Secrets manager](https://docs.flyte.org/en/latest/user_guide/productionizing/secrets.html).
# %%
SECRET_KEY = "wandb-api-key"
SECRET_GROUP = "wandb-api-group"

# %% [markdown]
# Next, we use `ImageSpec` to construct a container that contains the dependencies for this
# task:
# %%
REGISTRY = "localhost:30000"

image = ImageSpec(
    name="wandb_example",
    python_version="3.11",
    packages=["flytekitplugins-wandb", "xgboost", "scikit-learn"],
    registry=REGISTRY,
)


# %%
# The `wandb_init` decorator calls `wandb.init` and configures it to use Flyte's
# execution id as Weight and Biases run id. The body of the task is XGBoost training
# code, where we pass `WandbCallback` into `XGBClassifier`'s `callbacks`.
@task(
    container_image=image,
    secret_requests=[Secret(key=SECRET_KEY, group=SECRET_GROUP)],
)
@wandb_init(
    project=WANDB_PROJECT,
    entity=WANDB_ENTITY,
    secret_key=SECRET_KEY,
    secret_group=SECRET_GROUP,
)
def train() -> float:
    import wandb
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from wandb.integration.xgboost import WandbCallback
    from xgboost import XGBClassifier

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    bst = XGBClassifier(
        n_estimators=100,
        objective="binary:logistic",
        callbacks=[WandbCallback(log_model=True)],
    )
    bst.fit(X_train, y_train)

    test_score = bst.score(X_test, y_test)

    # Log custom metrics
    wandb.run.log({"test_score": test_score})
    return test_score


@workflow
def wf() -> float:
    return train()


# %% [markdown]
# To enable dynamic log links add plugin to Flyte's configuration file:
# ```yaml
# dynamic-log-links:
#    - wandb-execution-id:
#        displayName: Weights & Biases
#        templateUris: '{{ .taskConfig.host }}/{{ .taskConfig.entity }}/{{ .taskConfig.project }}/runs/{{ .executionName }}-{{ .nodeId }}-{{ .taskRetryAttempt }}'
#    - wandb-custom-id:
#        displayName: Weights & Biases
#        templateUris: '{{ .taskConfig.host }}/{{ .taskConfig.entity }}/{{ .taskConfig.project }}/runs/{{ .taskConfig.id }}'
# ```
