# %% [markdown]
# (slurm_agent_example_usage)=
#
# # Slurm agent example usage
# The Slurm agent enables seamless integration between Flyte workflows and Slurm-managed high-performance computing (HPC) clusters, allowing users to take advantage of Slurm’s powerful resource allocation, scheduling, and monitoring capabilities.
#
# The following examples demonstrate how to run different types of tasks using the Slurm agent, covering both basic and advanced use cases. Let’s start by importing the necessary packages.
# %%
import os

from flytekit import task, workflow
from flytekitplugins.slurm import Slurm, SlurmFunction, SlurmRemoteScript, SlurmShellTask, SlurmTask

# %% [markdown]
# ## `SlurmTask`
# First, `SlurmTask` is the most basic use case, allowing users to directly run a pre-existing shell script on the Slurm cluster. To configure this task, you need to specify the following fields:
# * `ssh_config`: Options of SSH client connection.
#     * Authentication is done via key pair verification. For available options, please refer to [here](https://github.com/JiangJiaWei1103/flytekit/blob/d0d59d3f809bad89a7567ce49d95c84c3f38bf5f/plugins/flytekit-slurm/flytekitplugins/slurm/ssh_utils.py#L21-L39).
# * `batch_script_path`: Path to the shell script on the Slurm cluster.
# * `sbatch_conf` (optional): Options of `sbatch` command. If not provided, defaults to an empty dict.
#     * For available options, please refer to the [official Slurm documentation](https://slurm.schedmd.com/sbatch.html).
# * `batch_script_args` (optional): Additional arguments for the batch script on Slurm cluster.
# %%
slurm_task = SlurmTask(
    name="basic",
    task_config=SlurmRemoteScript(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "job0",
        },
        batch_script_path="/home/ubuntu/echo.sh",
    ),
)


@workflow
def basic_wf() -> None:
    slurm_task()


# %% [markdown]
# Then, you can execute the workflow locally as below:
# %%
if __name__ == "__main__":
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(">>> LOCAL EXEC <<<")
    result = runner.invoke(pyflyte.main, ["run", path, "basic_wf"])
    print(result.output)


# %% [markdown]
# ## `SlurmShellTask`
# Instead of running a pre-existing shell script on the Slurm cluster, `SlurmShellTask` allows users to define the script content within the interface as shown below:
# %%
shell_task = SlurmShellTask(
    name="shell",
    script="""#!/bin/bash -i

echo [TEST SLURM SHELL TASK 1] Run the user-defined script...
""",
    task_config=Slurm(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
            "client_keys": ["~/.ssh/private_key.pem"],
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "job1",
        },
    ),
)


shell_task_with_args = SlurmShellTask(
    name="shell",
    script="""#!/bin/bash -i

echo [TEST SLURM SHELL TASK 2] Run the user-defined script with args...
echo Arg1: $1
echo Arg2: $2
echo Arg3: $3
""",
    task_config=Slurm(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "job2",
        },
        batch_script_args=["0", "a", "xyz"],
    ),
)


@workflow
def shell_wf() -> None:
    shell_task()
    shell_task_with_args()


# %% [markdown]
# Once again, execute the workflow locally to view the results:
# %%
if __name__ == "__main__":
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(">>> LOCAL EXEC <<<")
    result = runner.invoke(pyflyte.main, ["run", path, "shell_wf"])
    print(result.output)


# %% [markdown]
# ## `SlurmFunctionTask`
# Finally, `SlurmFunctionTask` is a highly flexible task type that allows you to run a user-defined task function on a Slurm cluster. To configure this task, you need to specify the following fields:
# * `ssh_config`: Options of SSH client connection.
#     * Authentication is done via key pair verification. For available options, please refer to [here](https://github.com/JiangJiaWei1103/flytekit/blob/d0d59d3f809bad89a7567ce49d95c84c3f38bf5f/plugins/flytekit-slurm/flytekitplugins/slurm/ssh_utils.py#L21-L39).
# * `sbatch_conf` (optional): Options of `sbatch` command. If not provided, defaults to an empty dict.
#     * For available options, please refer to the [official Slurm documentation](https://slurm.schedmd.com/sbatch.html).
# * `script` (optional): A user-defined script where `{task.fn}` serves as a placeholder for the task function execution.
#     * You should insert `{task.fn}` at the desired execution point within the script. If no script is provided, the task function will be executed directly.
# %%
@task(
    task_config=SlurmFunction(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
            "client_keys": ["~/.ssh/private_key.pem"],
        },
        sbatch_conf={"partition": "debug", "job-name": "job3", "output": "/home/ubuntu/fn_task.log"},
        script="""#!/bin/bash -i

echo [TEST SLURM FN TASK 1] Run the first user-defined task function...

# Setup env vars
export MY_ENV_VAR=123

# Source the virtual env
. /home/ubuntu/.cache/pypoetry/virtualenvs/demo-4A8TrTN7-py3.12/bin/activate

# Run the user-defined task function
{task.fn}
""",
    )
)
def plus_one(x: int) -> int:
    print(os.getenv("MY_ENV_VAR"))
    return x + 1


@task(
    task_config=SlurmFunction(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
        },
        script="""#!/bin/bash -i

echo [TEST SLURM FN TASK 2] Run the second user-defined task function...

. /home/ubuntu/.cache/pypoetry/virtualenvs/demo-4A8TrTN7-py3.12/bin/activate
{task.fn}
""",
    )
)
def greet(year: int) -> str:
    return f"Hello {year}!!!"


@workflow
def function_wf(x: int) -> str:
    x = plus_one(x=x)
    msg = greet(year=x)
    return msg


# %% [markdown]
# Let's execute the workflow:
# %%
if __name__ == "__main__":
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(">>> LOCAL EXEC <<<")
    result = runner.invoke(
        pyflyte.main, ["run", "--raw-output-data-prefix", "s3://my-flyte-slurm-agent", path, "function_wf", "--x", 2024]
    )
    print(result.output)


# %% [markdown]
# ## Train and Evaluate a DL Model with `SlurmFunctionTask`
# The following example demonstrates how `SlurmFunctionTask` can be integrated into a standard deep learning model training workflow. At the highest level, this workflow consists of three main components:
# * `dataset`: Manage dataset downloading and data preprocessing (MNIST is used as an example).
# * `model`: Define the deep learning model architecture (e.g., a convolutional neural network).
# * `trainer`: Handle the training process, including `train_epoch` and `eval_epoch`.
#
# Let’s first take a closer look at each component before diving into the main training workflow.
#
# ### Dataset
# %%
from typing import Tuple

from torch.utils.data import Dataset
from torchvision import datasets, transforms


def get_dataset(download_path: str = "/tmp/torch_data") -> Tuple[Dataset, Dataset]:
    """Process data and build training and validation sets.

    Args:
        download_path: Directory to store the raw data.

    Returns:
        A tuple (tr_ds, val_ds), where tr_ds is a training set and val_ds is a valiation set.
    """
    # Define data processing pipeline
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    tr_ds = datasets.MNIST(root=download_path, train=True, download=True, transform=transform)
    val_ds = datasets.MNIST(root=download_path, train=True, download=True, transform=transform)

    return tr_ds, val_ds


# %% [markdown]
# ### Model
# %%
from typing import Dict

import torch.nn as nn
from torch import Tensor


class Model(nn.Module):
    def __init__(self) -> None:
        super(Model, self).__init__()

        self.cnn_encoder = nn.Sequential(
            # Block 1
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            # Block 2
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.clf = nn.Linear(32 * 4 * 4, 10)

    def forward(self, inputs: Dict[str, Tensor]) -> Tensor:
        x = inputs["x"]
        bs = x.size(0)

        x = self.cnn_encoder(x)
        x = x.reshape(bs, -1)
        logits = self.clf(x)

        return logits


# %% [markdown]
# ### Trainer
# %%
import gc
from typing import Tuple

import torch
import torch.nn as nn
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm


def train_epoch(
    tr_loader: DataLoader, model: nn.Module, loss_fn: nn.Module, optimizer: Optimizer, debug: bool = False
) -> float:
    """Run training for one epoch.

    Args:
        tr_loader: Training dataloader.
        model: Model instance.
        loss_fn: Loss criterion.
        optimizer: Optimizer.
        debug: If True, run one batch only.

    Returns:
        The average training loss over batches.
    """
    tr_loss_tot = 0.0

    model.train()
    for i, batch_data in tqdm(enumerate(tr_loader), total=len(tr_loader)):
        optimizer.zero_grad(set_to_none=True)

        # Retrieve batched raw data
        x, y = batch_data
        inputs = {"x": x}

        # Forward pass
        logits = model(inputs)

        # Derive loss
        loss = loss_fn(logits, y)
        tr_loss_tot += loss.item()

        # Backpropagation
        loss.backward()

        optimizer.step()

        del x, y, inputs, logits
        _ = gc.collect()

        if debug:
            break

    tr_loss_avg = tr_loss_tot / len(tr_loader)

    return tr_loss_avg


@torch.no_grad()
def eval_epoch(
    eval_loader: DataLoader, model: nn.Module, loss_fn: nn.Module, debug: bool = False
) -> Tuple[float, float]:
    """Run evaluation for one epoch.

    Args:
        eval_loader: Evaluation dataloader.
        model: Model instance.
        loss_fn: Loss criterion.
        debug: If True, run one batch only.

    Returns:
        A tuple (eval_loss_avg, acc), where eval_loss_avg is the average evaluation loss over batches
        and acc is the accuracy.
    """
    eval_loss_tot = 0
    y_true, y_pred = [], []

    model.eval()
    for i, batch_data in tqdm(enumerate(eval_loader), total=len(eval_loader)):
        # Retrieve batched raw data
        x, y = batch_data
        inputs = {"x": x}

        # Forward pass
        logits = model(inputs)

        # Derive loss
        loss = loss_fn(logits, y)
        eval_loss_tot += loss.item()

        # Record batched output
        y_true.append(y.detach())
        y_pred.append(logits.detach())

        del x, y, inputs, logits
        _ = gc.collect()

        if debug:
            break

    eval_loss_avg = eval_loss_tot / len(eval_loader)

    # Derive accuracy
    y_true = torch.cat(y_true, dim=0)
    y_pred = torch.cat(y_pred, dim=0)
    y_pred = torch.argmax(y_pred, dim=1)
    acc = (y_true == y_pred).sum() / len(y_true)

    return eval_loss_avg, acc
