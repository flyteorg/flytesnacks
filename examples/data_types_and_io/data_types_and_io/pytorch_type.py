# PyTorch type
import torch
from flytekit import task, workflow


@task
def generate_tensor_2d() -> torch.Tensor:
    return torch.tensor([[1.0, -1.0, 2], [1.0, -1.0, 9], [0, 7.0, 3]])


@task
def reshape_tensor(tensor: torch.Tensor) -> torch.Tensor:
    # convert 2D to 3D
    tensor.unsqueeze_(-1)
    return tensor.expand(3, 3, 2)


@task
def generate_module() -> torch.nn.Module:
    bn = torch.nn.BatchNorm1d(3, track_running_stats=True)
    return bn


@task
def get_model_weight(model: torch.nn.Module) -> torch.Tensor:
    return model.weight


class MyModel(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.l0 = torch.nn.Linear(4, 2)
        self.l1 = torch.nn.Linear(2, 1)

    def forward(self, input):
        out0 = self.l0(input)
        out0_relu = torch.nn.functional.relu(out0)
        return self.l1(out0_relu)


@task
def get_l1() -> torch.nn.Module:
    model = MyModel()
    return model.l1


@workflow
def pytorch_native_wf():
    reshape_tensor(tensor=generate_tensor_2d())
    get_model_weight(model=generate_module())
    get_l1()


# Checkpoint
#
# `PyTorchCheckpoint` is a specialized checkpoint used for serializing and deserializing PyTorch models.
# It checkpoints `torch.nn.Module`'s state, hyperparameters and optimizer state.
#
# This module checkpoint differs from the standard checkpoint as it specifically captures the module's `state_dict`.
# Therefore, when restoring the module, the module's `state_dict` must be used in conjunction with the actual module.
# According to the PyTorch docs (https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-entire-model),
# it's recommended to store the module's `state_dict` rather than the module itself,
# although the serialization should work in either case.
from dataclasses import dataclass

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from dataclasses_json import dataclass_json
from flytekit.extras.pytorch import PyTorchCheckpoint


@dataclass_json
@dataclass
class Hyperparameters:
    epochs: int
    loss: float


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


@task
def generate_model(hyperparameters: Hyperparameters) -> PyTorchCheckpoint:
    bn = Net()
    optimizer = optim.SGD(bn.parameters(), lr=0.001, momentum=0.9)
    return PyTorchCheckpoint(module=bn, hyperparameters=hyperparameters, optimizer=optimizer)


@task
def load(checkpoint: PyTorchCheckpoint):
    new_bn = Net()
    new_bn.load_state_dict(checkpoint["module_state_dict"])
    optimizer = optim.SGD(new_bn.parameters(), lr=0.001, momentum=0.9)
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])


@workflow
def pytorch_checkpoint_wf():
    checkpoint = generate_model(hyperparameters=Hyperparameters(epochs=10, loss=0.1))
    load(checkpoint=checkpoint)
