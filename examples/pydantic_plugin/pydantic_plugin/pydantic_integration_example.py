# %% [markdown]
# (pydantic_integration_example)=
#
# # Pydantic Integration Example
#
# Pydantic is a data validation and settings management library for Python, enabling the creation of data models with type annotations.
#
# Flyte leverages Pydantic for robust input validation and serialization, ensuring that task inputs are correctly structured.

# %%
from typing import List

from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from pydantic.v1 import BaseModel


# %% [markdown]
# Let's first define a Pydantic model for training configuration.
# %%
class TrainConfig(BaseModel):
    lr: float = 1e-3  # Learning rate
    batch_size: int = 32  # Batch size for training
    files: List[FlyteFile]  # List of file inputs for training


# %% [markdown]
# Next, we use the Pydantic model in a Flyte task to train a model.
# %%
@task
def train(cfg: TrainConfig):
    print(f"Training with learning rate: {cfg.lr} and batch size: {cfg.batch_size}")
    for file in cfg.files:
        print(f"Processing file: {file}")


# %% [markdown]
# Now we define a Flyte workflow that utilizes the training task.
# %%
@workflow
def training_workflow(lr: float = 1e-3, batch_size: int = 32, files: List[FlyteFile] = []):
    cfg = TrainConfig(lr=lr, batch_size=batch_size, files=files)
    train(cfg=cfg)


# %% [markdown]
# Finally, we execute the workflow with sample parameters.
# %%
if __name__ == "__main__":
    training_workflow(lr=1e-3, batch_size=32, files=[FlyteFile(path="path/to/your/file")])
