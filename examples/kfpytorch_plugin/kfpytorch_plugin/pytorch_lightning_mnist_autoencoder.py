# %% [markdown]
# # Use PyTorch Lightning to Train an MNIST Autoencoder
#
# This notebook demonstrates how to use Pytorch Lightning with Flyte's `Elastic`
# task config, which is exposed by the `flytekitplugins-kfpytorch` plugin.
#
# First, we import all of the relevant packages.

import os

import lightning as L
from flytekit import ImageSpec, PodTemplate, Resources, task, workflow
from flytekit.extras.accelerators import T4
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.kfpytorch.task import Elastic
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor

# %% [markdown]
# ## Image and Pod Template Configuration
#
# For this task, we're going to use a custom image that has all of the
# necessary dependencies installed.

custom_image = ImageSpec(
    name="flytesnacks-lightning",
    packages=[
        "adlfs==2024.4.1",
        "gcsfs==2024.3.1",
        "torch==2.2.1",
        "torchvision",
        "flytekitplugins-kfpytorch",
        "kubernetes",
        "lightning==2.2.4",
        "networkx==3.2.1",
        "s3fs==2024.3.1",
    ],
    cuda="12.1.0",
    python_version="3.9",
    registry="nielsbantilan",
)

# %% [markdown]
# We're also going to define a custom pod template that mounts a shared memory
# volume to `/dev/shm`. This is necessary for distributed data parallel (DDP)
# training so that state can be shared across workers.

container = V1Container(name=custom_image.name, volume_mounts=[V1VolumeMount(mount_path="/dev/shm", name="dshm")])
volume = V1Volume(name="dshm", empty_dir=V1EmptyDirVolumeSource(medium="Memory"))
custom_pod_template = PodTemplate(
    primary_container_name=custom_image.name,
    pod_spec=V1PodSpec(containers=[container], volumes=[volume]),
)

# %% [markdown]
# ## Define a `LightningModule``
#
# Then we create a pytorch lightning module, which defines an autoencoder that
# will learn how to create compressed embeddings of MNIST images.


class MNISTAutoEncoder(L.LightningModule):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder

    def training_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        z = self.encoder(x)
        x_hat = self.decoder(z)
        loss = nn.functional.mse_loss(x_hat, x)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


# %% [markdown]
# ## Define a `LightningDataModule`
#
# Then we define a pytorch lightning data module, which defines how to prepare
# and setup the training data.


class MNISTDataModule(L.LightningDataModule):
    def __init__(self, root_dir, batch_size=64, dataloader_num_workers=0):
        super().__init__()
        self.root_dir = root_dir
        self.batch_size = batch_size
        self.dataloader_num_workers = dataloader_num_workers

    def prepare_data(self):
        MNIST(self.root_dir, train=True, download=True)

    def setup(self, stage=None):
        self.dataset = MNIST(
            self.root_dir,
            train=True,
            download=False,
            transform=ToTensor(),
        )

    def train_dataloader(self):
        persistent_workers = self.dataloader_num_workers > 0
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            num_workers=self.dataloader_num_workers,
            persistent_workers=persistent_workers,
            pin_memory=True,
            shuffle=True,
        )


# %% [markdown]
# ## Creating the pytorch `Elastic` task
#
# With the model architecture defined, we now create a Flyte task that assumes
# a world size of 16: 2 nodes with 8 devices each. We also set the `max_restarts`
# to `3` so that the task can be retried up to 3 times in case it fails for
# whatever reason, and we set `rdzv_configs` to have a generous timeout so that
# the head and worker nodes have enought time to connect to each other.
#
# This task will output a {ref}`FlyteDirectory <folder>`, which will contain the
# model checkpoint that will result from training.

NUM_NODES = 2
NUM_DEVICES = 8


@task(
    container_image=custom_image,
    task_config=Elastic(
        nnodes=NUM_NODES,
        nproc_per_node=NUM_DEVICES,
        rdzv_configs={"timeout": 36000, "join_timeout": 36000},
        max_restarts=3,
    ),
    accelerator=T4,
    requests=Resources(mem="32Gi", cpu="48", gpu="8", ephemeral_storage="100Gi"),
    pod_template=custom_pod_template,
)
def train_model(dataloader_num_workers: int) -> FlyteDirectory:
    """Train an autoencoder model on the MNIST."""

    encoder = nn.Sequential(nn.Linear(28 * 28, 64), nn.ReLU(), nn.Linear(64, 3))
    decoder = nn.Sequential(nn.Linear(3, 64), nn.ReLU(), nn.Linear(64, 28 * 28))
    autoencoder = MNISTAutoEncoder(encoder, decoder)

    root_dir = os.getcwd()
    data = MNISTDataModule(
        root_dir,
        batch_size=4,
        dataloader_num_workers=dataloader_num_workers,
    )

    model_dir = os.path.join(root_dir, "model")
    trainer = L.Trainer(
        default_root_dir=model_dir,
        max_epochs=3,
        num_nodes=NUM_NODES,
        devices=NUM_DEVICES,
        accelerator="gpu",
        strategy="ddp",
        precision="16-mixed",
    )
    trainer.fit(model=autoencoder, datamodule=data)
    return FlyteDirectory(path=str(model_dir))


# %% [markdown]
# Finally, we wrap it all up in a workflow.


@workflow
def train_workflow(dataloader_num_workers: int = 1) -> FlyteDirectory:
    return train_model(dataloader_num_workers=dataloader_num_workers)
