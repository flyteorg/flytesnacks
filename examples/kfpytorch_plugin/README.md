(kf-pytorch-op)=

# PyTorch Distributed

```{eval-rst}
.. tags:: Integration, DistributedComputing, MachineLearning, KubernetesOperator, Advanced
```

The Kubeflow PyTorch plugin leverages the [Kubeflow training operator](https://github.com/kubeflow/training-operator)
to offer a highly streamlined interface for conducting distributed training using different PyTorch backends.

## Install the plugin

To use the PyTorch plugin, run the following command:

```
pip install flytekitplugins-kfpytorch
```

To enable the plugin in the backend, follow instructions outlined in the {ref}`deployment-plugin-setup-k8s` guide.

## Run the example on the Flyte cluster

To run the provided examples on the Flyte cluster, use the following commands:

Distributed pytorch training:

```
pyflyte run --remote pytorch_mnist.py pytorch_training_wf
```

Pytorch lightning training:

```
pyflyte run --remote pytorch_lightning_mnist_autoencoder.py train_workflow
```

```{auto-examples-toc}
pytorch_mnist
pytorch_lightning_mnist_autoencoder
```
