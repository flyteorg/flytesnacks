# %% [markdown]
# (comet_ml_example)=
#
# # Comet Example
# Comet’s machine learning platform integrates with your existing infrastructure and
# tools so you can manage, visualize, and optimize models from training runs to
# production monitoring. This plugin integrates Flyte with Comet by configuring
# links between the two platforms.
import os
import os.path

from flytekit import (
    ImageSpec,
    Secret,
    current_context,
    task,
    workflow,
)
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.comet_ml import comet_ml_login

# %% [markdown]
# First, we specify the project and workspace that we will use with Comet's platform
# Please update `PROJECT_NAME` and `WORKSPACE` to the values associated with your account.
# %%
PROJECT_NAME = "flytekit-comet-ml-v1"
WORKSPACE = "thomas-unionai"

# %% [markdown]
# W&B requires an API key to authenticate with Comet. In the above example,
# the secret is created using
# [Flyte's Secrets manager](https://docs.flyte.org/en/latest/user_guide/productionizing/secrets.html).
# %%
secret = Secret(key="comet-ml-key", group="comet-ml-group")

# %% [markdown]
# Next, we use `ImageSpec` to construct a container that contains the dependencies for this
# task:
# %%

REGISTRY = os.getenv("REGISTRY", "localhost:30000")
image = ImageSpec(
    name="comet-ml",
    packages=[
        "torch==2.3.1",
        "comet-ml==3.43.2",
        "lightning==2.3.0",
        "flytekitplugins-comet-ml",
        "torchvision",
    ],
    builder="default",
    registry=REGISTRY,
)


# %% [markdown]
# Here, we use a Flyte task to download the dataset and cache it:
# %%
@task(cache=True, cache_version="2", container_image=image)
def get_dataset() -> FlyteDirectory:
    from torchvision.datasets import MNIST

    ctx = current_context()
    dataset_dir = os.path.join(ctx.working_directory, "datasetset")
    os.makedirs(dataset_dir, exist_ok=True)

    # Download training and evaluation dataset
    MNIST(dataset_dir, train=True, download=True)
    MNIST(dataset_dir, train=False, download=True)

    return dataset_dir


# %%
# The `comet_ml_login` decorator calls `comet_ml.init` and configures it to use Flyte's
# execution id as the Comet's experiment key. The body of the task is PyTorch Lightning
# training code, where we pass `CometLogger` into the `Trainer`'s `logger`.
@task(
    secret_requests=[secret],
    container_image=image,
)
@comet_ml_login(
    project_name=PROJECT_NAME,
    workspace=WORKSPACE,
    secret=secret,
)
def train_lightning(dataset: FlyteDirectory, hidden_layer_size: int):
    import pytorch_lightning as pl
    import torch
    import torch.nn.functional as F
    from pytorch_lightning import Trainer
    from pytorch_lightning.loggers import CometLogger
    from torch.utils.data import DataLoader
    from torchvision import transforms
    from torchvision.datasets import MNIST

    class Model(pl.LightningModule):
        def __init__(self, layer_size=784, hidden_layer_size=256):
            super().__init__()
            self.save_hyperparameters()
            self.layers = torch.nn.Sequential(
                torch.nn.Linear(layer_size, hidden_layer_size),
                torch.nn.Linear(hidden_layer_size, 10),
            )

        def forward(self, x):
            return torch.relu(self.layers(x.view(x.size(0), -1)))

        def training_step(self, batch, batch_nb):
            x, y = batch
            loss = F.cross_entropy(self(x), y)
            self.logger.log_metrics({"train_loss": loss}, step=batch_nb)
            return loss

        def validation_step(self, batch, batch_nb):
            x, y = batch
            y_hat = self.forward(x)
            loss = F.cross_entropy(y_hat, y)
            self.logger.log_metrics({"val_loss": loss}, step=batch_nb)
            return loss

        def configure_optimizers(self):
            return torch.optim.Adam(self.parameters(), lr=0.02)

    dataset.download()
    train_ds = MNIST(dataset, train=True, download=False, transform=transforms.ToTensor())
    eval_ds = MNIST(dataset, train=False, download=False, transform=transforms.ToTensor())
    train_loader = DataLoader(train_ds, batch_size=32)
    eval_loader = DataLoader(eval_ds, batch_size=32)

    comet_logger = CometLogger()
    comet_logger.log_hyperparams({"batch_size": 32})

    model = Model(hidden_layer_size=hidden_layer_size)
    trainer = Trainer(max_epochs=1, fast_dev_run=True, logger=comet_logger)
    trainer.fit(model, train_loader, eval_loader)


@workflow
def main(hidden_layer_size: int = 32):
    dataset = get_dataset()
    train_lightning(dataset=dataset, hidden_layer_size=hidden_layer_size)


# %% [markdown]
# To enable dynamic log links, add plugin to Flyte's configuration file:
# ```yaml
# plugins:
#   logs:
#     dynamic-log-links:
#       - comet-ml-execution-id:
#           displayName: Comet
#           templateUris: "{{ .taskConfig.host }}/{{ .taskConfig.workspace }}/{{ .taskConfig.project_name }}/{{ .executionName }}{{ .nodeId }}{{ .taskRetryAttempt }}{{ .taskConfig.link_suffix }}"
#       - comet-ml-custom-id:
#           displayName: Comet
#           templateUris: "{{ .taskConfig.host }}/{{ .taskConfig.workspace }}/{{ .taskConfig.project_name }}/{{ .taskConfig.experiment_key }}"
# ```
