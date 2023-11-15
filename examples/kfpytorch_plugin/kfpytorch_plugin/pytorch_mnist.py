# %% [markdown]
# # Run PyTorch Distributed
#
# This example is based on the default MNIST example found in the Kubeflow's PyTorch guide
# [here](https://github.com/kubeflow/training-operator/blob/master/examples/pytorch/mnist/mnist.py).
#
# To begin, import the required dependencies.
# %%
import os
import typing
from dataclasses import dataclass
from typing import Tuple

import flytekit
from dataclasses_json import dataclass_json
from flytekit import ImageSpec, Resources, task, workflow
from flytekit.types.directory import TensorboardLogs
from flytekit.types.file import PNGImageFile, PythonPickledFile

WORLD_SIZE = int(os.environ.get("WORLD_SIZE", 1))

# %% [markdown]
# Create an `ImageSpec` to encompass all the dependencies needed for the PyTorch task.
# %%
custom_image = ImageSpec(
    name="flyte-kfpytorch-plugin",
    packages=["torch", "torchvision", "flytekitplugins-kfpytorch", "matplotlib", "tensorboardX"],
    registry="ghcr.io/flyteorg",
)

# %% [markdown]
# :::{important}
# Replace `ghcr.io/flyteorg` with a container registry you've access to publish to.
# To upload the image to the local registry in the demo cluster, indicate the registry as `localhost:30000`.
# :::
#
# The following imports are required to configure the PyTorch cluster in Flyte.
# You can load them on demand.
# %%
if custom_image.is_container():
    import matplotlib.pyplot as plt
    import torch
    import torch.nn.functional as F
    from flytekitplugins.kfpytorch import PyTorch, Worker
    from tensorboardX import SummaryWriter
    from torch import distributed as dist
    from torch import nn, optim
    from torchvision import datasets, transforms

# %% [markdown]
# You can activate GPU support by either using the base image that includes the necessary GPU dependencies
# or by initializing the [CUDA parameters](https://github.com/flyteorg/flytekit/blob/master/flytekit/image_spec/image_spec.py#L34-L35)
# within the `ImageSpec`.
#
# Adjust memory, GPU usage and storage settings based on whether you are
# registering against the demo cluster or not.
# %%
if os.getenv("SANDBOX") != "":
    cpu_request = "500m"
    mem_request = "500Mi"
    gpu_request = "0"
    mem_limit = "500Mi"
    gpu_limit = "0"
else:
    cpu_request = "500m"
    mem_request = "4Gi"
    gpu_request = "1"
    mem_limit = "8Gi"
    gpu_limit = "1"


# %% [markdown]
# In this example, we create a model.
# %%
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


# %% [markdown]
# We define a trainer.
# %%
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


# %% [markdown]
# We define a test function to test the trained model.
# %%
def test(model, device, test_loader, writer, epoch):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction="sum").item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print("\naccuracy={:.4f}\n".format(float(correct) / len(test_loader.dataset)))
    accuracy = float(correct) / len(test_loader.dataset)
    writer.add_scalar("accuracy", accuracy, epoch)
    return accuracy


# %% [markdown]
# We define a couple of auxiliary functions, initialize hyperparameters
# and create a `NamedTuple` to capture the outputs of the PyTorch task.
# %%
def epoch_step(model, device, train_loader, test_loader, optimizer, epoch, writer, log_interval):
    train(model, device, train_loader, optimizer, epoch, writer, log_interval)
    return test(model, device, test_loader, writer, epoch)


def should_distribute():
    return dist.is_available() and WORLD_SIZE > 1


def is_distributed():
    return dist.is_available() and dist.is_initialized()


@dataclass_json
@dataclass
class Hyperparameters(object):
    """
    Args:
        backend: Distributed backend to use
        sgd_momentum: SGD momentum (default: 0.5)
        seed: random seed (default: 1)
        log_interval: how many batches to wait for before logging training status
        batch_size: input batch size for training (default: 64)
        test_batch_size: input batch size for testing (default: 1000)
        epochs: number of epochs to train (default: 10)
        learning_rate: learning rate (default: 0.01)
    """

    backend: str = dist.Backend.GLOO
    sgd_momentum: float = 0.5
    seed: int = 1
    log_interval: int = 10
    batch_size: int = 64
    test_batch_size: int = 1000
    epochs: int = 10
    learning_rate: float = 0.01


TrainingOutputs = typing.NamedTuple(
    "TrainingOutputs",
    epoch_accuracies=typing.List[float],
    model_state=PythonPickledFile,
    logs=TensorboardLogs,
)


# %% [markdown]
# To create a PyTorch task, add {py:class}`~flytekitplugins.kfpytorch.PyTorch` config to the Flyte task.
# %%
@task(
    task_config=PyTorch(worker=Worker(replicas=2)),
    retries=2,
    cache=True,
    cache_version="0.1",
    requests=Resources(cpu=cpu_request, mem=mem_request, gpu=gpu_request),
    limits=Resources(mem=mem_limit, gpu=gpu_limit),
    container_image=custom_image,
)
def mnist_pytorch_job(hp: Hyperparameters) -> TrainingOutputs:
    log_dir = os.path.join(flytekit.current_context().working_directory, "logs")
    writer = SummaryWriter(log_dir)

    torch.manual_seed(hp.seed)

    use_cuda = torch.cuda.is_available()
    print(f"Use cuda {use_cuda}")
    device = torch.device("cuda" if use_cuda else "cpu")

    print("Using device: {}, world size: {}".format(device, WORLD_SIZE))

    if should_distribute():
        print("Using distributed PyTorch with {} backend".format(hp.backend))
        dist.init_process_group(backend=hp.backend)

    # Load data
    kwargs = {"num_workers": 1, "pin_memory": True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            os.path.join(flytekit.current_context().working_directory, "data"),
            train=True,
            download=True,
            transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]),
        ),
        batch_size=hp.batch_size,
        shuffle=True,
        **kwargs,
    )
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            os.path.join(flytekit.current_context().working_directory, "data"),
            train=False,
            transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]),
        ),
        batch_size=hp.test_batch_size,
        shuffle=False,
        **kwargs,
    )

    # Train the model
    model = Net().to(device)

    if is_distributed():
        Distributor = nn.parallel.DistributedDataParallel if use_cuda else nn.parallel.DistributedDataParallelCPU
        model = Distributor(model)

    optimizer = optim.SGD(model.parameters(), lr=hp.learning_rate, momentum=hp.sgd_momentum)

    accuracies = [
        epoch_step(
            model,
            device,
            train_loader,
            test_loader,
            optimizer,
            epoch,
            writer,
            hp.log_interval,
        )
        for epoch in range(1, hp.epochs + 1)
    ]

    # Save the model
    model_file = os.path.join(flytekit.current_context().working_directory, "mnist_cnn.pt")
    torch.save(model.state_dict(), model_file)

    return TrainingOutputs(
        epoch_accuracies=accuracies,
        model_state=PythonPickledFile(model_file),
        logs=TensorboardLogs(log_dir),
    )


# %% [markdown]
# The `torch.save` function is utilized to save the model's `state_dict` in accordance with the guidelines outlined in the
# [PyTorch documentation](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-and-loading-models).
# Typically, the file is given a `.pt` extension.
#
# Additionally, an output variable named `logs` will be generated.
# These logs can be employed for visualizing the training process in Tensorboard.
# They constitute the outcomes of the `SummaryWriter` interface.
# %%


# %% [markdown]
# Next, we generate an accuracy plot in the form of a PNG image.
# %%
@task(container_image=custom_image)
def plot_accuracy(epoch_accuracies: typing.List[float]) -> PNGImageFile:
    plt.plot(epoch_accuracies)
    plt.title("Accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    accuracy_plot = os.path.join(flytekit.current_context().working_directory, "accuracy.png")
    plt.savefig(accuracy_plot)
    return PNGImageFile(accuracy_plot)


# %% [markdown]
# In the end, we combine the training and plotting processes within a single pipeline.
# In this setup, the training is executed initially, succeeded by the accuracy plotting phase.
# Data is exchanged between these steps, and the workflow produces both the image and the serialized model as its outputs.
# %%
@workflow
def pytorch_training_wf(
    hp: Hyperparameters = Hyperparameters(epochs=2, batch_size=128),
) -> Tuple[PythonPickledFile, PNGImageFile, TensorboardLogs]:
    accuracies, model, logs = mnist_pytorch_job(hp=hp)
    plot = plot_accuracy(epoch_accuracies=accuracies)
    return model, plot, logs


# %% [markdown]
# Running the model locally requires minimal modifications,
# as long as the code handles the resolution of whether it should be run in a distributed manner or not.
# %%
if __name__ == "__main__":
    model, plot, logs = pytorch_training_wf()
    print(f"Model: {model}, plot PNG: {plot}, Tensorboard Log Dir: {logs}")

# %% [markdown]
# (pytorch_tensorboard)=
# :::{note}
# During local execution, the output of the process appears as follows:
#
# ```
# Model: /tmp/flyte/20210110_214129/mock_remote/8421ae4d041f76488e245edf3f4360d5/my_model.h5, plot PNG: /tmp/flyte/20210110_214129/mock_remote/cf6a2cd9d3ded89ed814278a8fb3678c/accuracy.png, Tensorboard Log Dir: /tmp/flyte/20210110_214129/mock_remote/a4b04e58e21f26f08f81df24094d6446/
# ```
#
# To visualize the training progress, utilize the Tensorboard log directory path as input for Tensorboard, as demonstrated below:
#
# ```
# tensorboard --logdir /tmp/flyte/20210110_214129/mock_remote/a4b04e58e21f26f08f81df24094d6446/
# ```
#
# When executing remotely on the Flyte-hosted environment, the workflow execution outputs can be retrieved.
# You can obtain the outputs, which will be in the form of a path to a storage system such as S3, GCS, Minio, etc.
# To visualize the outcomes, you can point Tensorboard on your local machine to these storage locations.
# :::
#
# ## Pytorch elastic training (torchrun)
#
# Flyte supports distributed training through [torch elastic](https://pytorch.org/docs/stable/elastic/run.html) using `torchrun`.
# You can carry out elastic training on a single node with a local worker group of size four,
# analogous to executing `torchrun --nproc-per-node=4 --nnodes=1 ....`.
#
# The process involves adding {py:class}`~flytekitplugins.kfpytorch.Elastic` configuration to the Flyte task.
#
# ```python
# from flytekitplugins.kfpytorch import Elastic
#
# @task(
#   task_config=Elastic(
#     nnodes=1,
#     nproc_per_node=4,
#   )
# )
# def task():
#     ...
# ```
#
# This initializes four worker processes, whether executed locally or remotely within a Kubernetes pod within a Flyte cluster.
# For distributed elastic training across multiple nodes, the Elastic task configuration can be utilized as follows:
#
# ```python
# from flytekitplugins.kfpytorch import Elastic
#
# @task(
#   task_config=Elastic(
#     nnodes=2,
#     nproc_per_node=4,
#   ),
# )
# def train():
# ```
#
# This configuration runs distributed training on two nodes, each with four worker processes.
#
# :::{note}
# In the context of distributed training, it's important to acknowledge that return values from various workers could potentially vary.
# If you need to regulate which worker's return value gets passed on to subsequent tasks in the workflow,
# you have the option to raise an
# [IgnoreOutputs exception](https://docs.flyte.org/projects/flytekit/en/latest/generated/flytekit.core.base_task.IgnoreOutputs.html)
# for all remaining ranks.
# :::
