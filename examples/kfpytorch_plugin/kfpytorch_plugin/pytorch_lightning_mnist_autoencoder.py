# %% [markdown]
# # Use PyTorch Lightning to Train an MNIST Autoencoder
#
# This notebook demonstrates how to use Pytorch Lightning with Flyte's `Elastic`
# task config, which is exposed by the `flytekitplugins-kfpytorch` plugin.
#
# First, we import all of the relevant packages.

import os

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
from torch import nn, optim, utils
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
volume = V1Volume(name="dshm", empty_dir=V1EmptyDirVolumeSource(medium="", size_limit="200Gi"))
custom_pod_template = PodTemplate(
    primary_container_name=custom_image.name,
    pod_spec=V1PodSpec(containers=[container], volumes=[volume]),
)

# %% [markdown]
# ## Define a Lightning Module
#
# Then we create a pytorch lightning module, which defines an autoencoder that
# will learn how to create compressed embeddings of MNIST images.


def create_model(encoder, decoder):
    import lightning as L

    class LitAutoEncoder(L.LightningModule):
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

    return LitAutoEncoder(encoder, decoder)


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

    import lightning as L

    encoder = nn.Sequential(nn.Linear(28 * 28, 64), nn.ReLU(), nn.Linear(64, 3))
    decoder = nn.Sequential(nn.Linear(3, 64), nn.ReLU(), nn.Linear(64, 28 * 28))
    autoencoder = create_model(encoder, decoder)

    root_dir = os.getcwd()
    dataset = MNIST(
        os.path.join(root_dir, "dataset"),
        download=True,
        transform=ToTensor(),
    )
    train_loader = utils.data.DataLoader(
        dataset, batch_size=1, pin_memory=True, persistent_workers=True, num_workers=dataloader_num_workers
    )

    model_dir = os.path.join(root_dir, "model")
    trainer = L.Trainer(
        default_root_dir=model_dir,
        max_epochs=100,
        num_nodes=NUM_NODES,
        devices=NUM_DEVICES,
        accelerator="gpu",
        strategy="ddp",
        precision=16,
    )
    trainer.fit(model=autoencoder, train_dataloaders=train_loader)
    return FlyteDirectory(path=str(model_dir))


# %% [markdown]
# Finally, we wrap it all up in a workflow.


@workflow
def train_workflow(dataloader_num_workers: int = 1) -> FlyteDirectory:
    return train_model(dataloader_num_workers=dataloader_num_workers)
