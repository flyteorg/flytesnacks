"""
Single Node GPU training
-------------------------
Training a model on a single node on one gpu is as trivial as writing any Flyte task and simply setting the GPU='1'.
As long as the docker image is built correctly with the right version of the GPU drivers and your Flyte backend is
provisioned to have GPU machines, Flyte will execute your task on a node that has GPU's.

Currently Flyte does not provide any specific task type for Pytorch (though it is entire possible to provide a task-type
that supports pytorch-ignite or pytorch-lightening support, but this is not critical). You can request for a GPU, simply
by setting the GPU="1" resource request and then at runtime you will receive a GPU.

This example shows how you can create any Pytorch model and train it using Flyte and your specialized container. Flyte
will handle the data passing and can export the model out of the training environment.

"""
import os
import typing
from dataclasses import dataclass

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from dataclasses_json import dataclass_json
from flytekit import Resources, task, workflow
from flytekit.types.directory import TensorboardLogs
from flytekit.types.file import PNGImageFile, PythonPickledFile
from tensorboardX import SummaryWriter
from torch import distributed as dist
from torch import nn, optim
from torchvision import datasets, transforms


WORLD_SIZE = int(os.environ.get("WORLD_SIZE", 1))


# %%
# Actual model
# ============
# this the Model class with all the layers
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


# %%
# Trainer
# =======
# This is the core training loop, which runs for 1 epoch. The loss values are written to the SummaryWriter
def train(model, device, train_loader, optimizer, epoch, writer, log_interval):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tloss={:.4f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )
            niter = epoch * len(train_loader) + batch_idx
            writer.add_scalar("loss", loss.item(), niter)


# %%
# Test the model
# ==============
# This method calculates the accuracy for the given model per epoch
def test(model, device, test_loader, writer, epoch):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[
                1
            ]  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print("\naccuracy={:.4f}\n".format(float(correct) / len(test_loader.dataset)))
    accuracy = float(correct) / len(test_loader.dataset)
    writer.add_scalar("accuracy", accuracy, epoch)
    return accuracy


def epoch_step(
        model, device, train_loader, test_loader, optimizer, epoch, writer, log_interval
):
    train(model, device, train_loader, optimizer, epoch, writer, log_interval)
    return test(model, device, test_loader, writer, epoch)


# %%
# Training Hyperparameters
# ========================
#
@dataclass_json
@dataclass
class Hyperparameters(object):
    """
    Args:
        batch_size: input batch size for training (default: 64)
        test_batch_size: input batch size for testing (default: 1000)
        epochs: number of epochs to train (default: 10)
        learning_rate: learning rate (default: 0.01)
        sgd_momentum: SGD momentum (default: 0.5)
        seed: random seed (default: 1)
        log_interval: how many batches to wait before logging training status
        dir: directory where summary logs are stored
    """

    backend: str = dist.Backend.GLOO
    sgd_momentum: float = 0.5
    seed: int = 1
    log_interval: int = 10
    batch_size: int = 64
    test_batch_size: int = 1000
    epochs: int = 10
    learning_rate: float = 0.01


# %%
# Actual Training algorithm
# =========================
# The output model using `torch.save` saves the `state_dict` as described
# `in pytorch docs <https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-and-loading-models>`_.
# A common convention is to have the ``.pt`` extension for the file
#
# Notice we are also generating an output variable called logs, these logs can be used to visualize the training in
# Tensorboard and are the output of the `SummaryWriter` interface
# Refer to section :ref:`pytorch_tensorboard` to visualize the outputs of this example.
#
# .. note::
#
#    Note the usage of requests=Resources(gpu="1"). This will force Flyte to allocate this task onto a machine with GPUs
#    The task will be queued up until a machine with gpu's can be procured. Also for the GPU Training to work, the
#    dockerfile needs to be built as explained in the :ref:`pytorch-training` section.
#
TrainingOutputs = typing.NamedTuple(
    "TrainingOutputs",
    epoch_accuracies=typing.List[float],
    model_state=PythonPickledFile,
    logs=TensorboardLogs,
)


@task(retries=2, cache=True, cache_version="1.0", requests=Resources(gpu="1"))
def train_mnist(hp: Hyperparameters) -> TrainingOutputs:
    log_dir = "logs"
    writer = SummaryWriter(log_dir)

    torch.manual_seed(hp.seed)

    # Ideally if GPU training is required, and if cuda is not available, we can raise an Exception, but as we want
    # this algorithm to work locally as well (and most users dont have a GPU locally), we will fallback to using a CPU
    use_cuda = torch.cuda.is_available()
    print(f"Use cuda {use_cuda}")
    device = torch.device("cuda" if use_cuda else "cpu")

    print("Using device: {}, world size: {}".format(device, WORLD_SIZE))

    # LOAD Data
    kwargs = {"num_workers": 1, "pin_memory": True} if use_cuda else {}
    training_data_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            "../data",
            train=True,
            download=True,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
            ),
        ),
        batch_size=hp.batch_size,
        shuffle=True,
        **kwargs,
    )
    test_data_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            "../data",
            train=False,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
            ),
        ),
        batch_size=hp.test_batch_size,
        shuffle=False,
        **kwargs,
    )

    # Train the model
    model = Net().to(device)

    optimizer = optim.SGD(
        model.parameters(), lr=hp.learning_rate, momentum=hp.sgd_momentum
    )

    # Run multiple epochs and capture the accuracies for each epoch
    accuracies = [
        epoch_step(
            model,
            device,
            train_loader=training_data_loader,
            test_loader=test_data_loader,
            optimizer=optimizer,
            epoch=epoch,
            writer=writer,
            log_interval=hp.log_interval,
        )
        for epoch in range(1, hp.epochs + 1)
    ]

    # After training the model, we can simply save it to disk and return it from the Flyte task as a FlyteFile type
    # called the PythonPickledFile. PythonPickledFile is simply a decorator on the FlyteFile, that records the format
    # of the serialized model as ``pickled``
    model_file = "mnist_cnn.pt"
    torch.save(model.state_dict(), model_file)

    return TrainingOutputs(
        epoch_accuracies=accuracies,
        model_state=PythonPickledFile(model_file),
        logs=TensorboardLogs(log_dir),
    )


# %%
# Let us plot the accuracy
# ========================
# We will output the accuracy plot as a PNG image
@task
def plot_accuracy(epoch_accuracies: typing.List[float]) -> PNGImageFile:
    # summarize history for accuracy
    plt.plot(epoch_accuracies)
    plt.title("Accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    accuracy_plot = "accuracy.png"
    plt.savefig(accuracy_plot)

    return PNGImageFile(accuracy_plot)


# %%
# Create a pipeline
# =================
# now the training and the plotting can be together put into a pipeline, in which case the training is performed first
# followed by the plotting of the accuracy. Data is passed between them and the workflow itself outputs the image and
# the serialize model
@workflow
def pytorch_training_wf(
        hp: Hyperparameters,
) -> (PythonPickledFile, PNGImageFile, TensorboardLogs):
    accuracies, model, logs = train_mnist(hp=hp)
    plot = plot_accuracy(epoch_accuracies=accuracies)
    return model, plot, logs


# %%
# Run the model locally
# =====================
# It is possible to run the model locally with almost no modifications (as long as the code takes care of the resolving
# if distributed or not)
if __name__ == "__main__":
    model, plot, logs = pytorch_training_wf(
        hp=Hyperparameters(epochs=2, batch_size=128)
    )
    print(f"Model: {model}, plot PNG: {plot}, Tensorboard Log Dir: {logs}")
