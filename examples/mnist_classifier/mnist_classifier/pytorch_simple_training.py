# %% [markdown]
# (pytorch_simple_training)=
#
# # Simple Showcase of training a vanilla PyTorch model on MNIST, using Flyte
#
# This example showcases how to leverage ImageSpec. This example shows quickly how to get started with Flyte,
# without any additional dependencies or frameworks.
#
# ## Prerequisites
# You will need to have both Docker installed, and you must login with `docker login` to an image registry such as ghcr.io, or DockerHub.
#

import torch
from torch.utils.data import DataLoader
from datetime import timedelta
from torchvision import datasets, transforms
from flytekit import task, workflow, Resources, ImageSpec, approve
import torch as th
from torch import nn
from typing import Tuple
"""
This example is a simple MNIST training example. It uses the PyTorch framework to train a simple CNN model on the MNIST dataset.
The model is trained for 10 epochs and the validation loss is calculated on the test set.
"""
imagespec = ImageSpec(
   name="flytekit",
   registry="ghcr.io/zeryx",
   base_image="ubuntu20.04",
   requirements="requirements.txt",
   cuda="11.2.2",
   cudnn="8",
   python_version="3.10"
)


@task(requests=Resources(cpu="1", mem="1Gi", ephemeral_storage="10Gi"), container_image=imagespec, retries=10)
def get_dataset(training: bool, gpu: bool = False) -> DataLoader:
    """
    This task returns the MNIST dataset. It is used by the training task to get the training and test set.
    training: bool
    gpu: bool
    """
    dataset = datasets.MNIST("/tmp/mnist", train=training, download=True, transform=transforms.ToTensor())
    if gpu and training is True:
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True, pin_memory_device="cuda", pin_memory=True)
    else:
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
    return dataloader


@task(container_image=imagespec,
      requests=Resources(cpu="2", mem="10Gi", ephemeral_storage="15Gi", gpu="1"))
def train(dataset: DataLoader, n_epochs: int) -> th.nn.Sequential:
    """
    This task trains the model for the specified number of epochs.
    This variant of the task uses the GPU for training. as you can see from the Resources requested in the task decorator.
    """
    model, optim = get_model_architecture()
    return train_model(model=model, optim=optim, dataset=dataset, n_epochs=n_epochs)


@task(requests=Resources(cpu="2", mem="10Gi", ephemeral_storage="15Gi"), container_image=imagespec)
def validation_loss(model: th.nn.Sequential, dataset: DataLoader) -> str:
    """
    This task calculates the validation loss on the test set.
    This is always run in CPU mode, regardless of the GPU setting. It simply returns the NNL Model Loss on the test set.
    """
    model.to("cpu").eval()
    losses = []
    with torch.no_grad():
        for data, target in dataset:
            data, target = data.to("cpu"), target.to("cpu")
            output = model.forward(data)
            loss = th.nn.functional.nll_loss(output, target)
            losses.append(loss.item())
    loss = 0
    for l in losses:
        loss += l
    loss = loss / len(losses)
    return "NLL model loss in test set: " + str(loss)


"""
General Functions, used by Tasks
"""


def train_model(model: th.nn.Sequential, optim: th.optim.Optimizer, dataset: DataLoader,
                n_epochs: int) -> th.nn.Sequential:
    """
    This function runs the inner training loop for the specified number of epochs.
    If a GPU is available, the model is moved to the GPU and the training is done on the GPU.
    """
    model = model.to("cuda").train()
    for epoch in range(n_epochs):
        for data, target in dataset:
            if th.cuda.is_available():
                data, target = data.to("cuda"), target.to("cuda")
            optim.zero_grad()
            output = model.forward(data)
            loss = th.nn.functional.cross_entropy(output, target)
            loss.backward()
            optim.step()
            print(f"Epoch {epoch + 1}/{n_epochs}, Loss: {loss.item()}")
    return model



def get_model_architecture() -> (th.nn.Sequential, th.optim.Optimizer):
    model = nn.Sequential(
        nn.Conv2d(1, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),
        nn.Conv2d(32, 512, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),
        nn.Flatten(),
        nn.Linear(512 * 7 * 7, 512),
        nn.ReLU(),
        nn.Linear(512, 10)
    )
    optimizer = th.optim.SGD(model.parameters(), lr=0.003, momentum=0.9)
    return model, optimizer


@workflow
def mnist_workflow_gpu(n_epoch: int = 10) -> Tuple[str, th.nn.Sequential]:
    """
    
    """
    training_dataset = get_dataset(training=True, gpu=True)
    test_dataset = get_dataset(training=False, gpu=True)
    trained_model = train(dataset=training_dataset, n_epochs=n_epoch)
    approve(trained_model, "Approve the model", timeout=timedelta(minutes=10))
    output = validation_loss(model=trained_model, dataset=test_dataset)
    return output, trained_model

