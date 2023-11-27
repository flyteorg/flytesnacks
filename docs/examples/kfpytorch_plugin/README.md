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

To enable the plugin in the backend, follow instructions outlined in the {std:ref}`flyte:deployment-plugin-setup-k8s` guide.

## Run the example on the Flyte cluster

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/kfpytorch_plugin/kfpytorch_plugin/pytorch_mnist.py \
  pytorch_training_wf
```

```{auto-examples-toc}
pytorch_mnist
```
