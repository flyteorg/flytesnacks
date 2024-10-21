(kf-mpi-op)=

# MPI

```{eval-rst}
.. tags:: Integration, DistributedComputing, MachineLearning, KubernetesOperator, Advanced
```

In this section, you'll find a demonstration of running Horovod code with the Kubeflow MPI API.

## Horovod

[Horovod](http://horovod.ai/) stands as a distributed deep learning training framework compatible with
TensorFlow, Keras, PyTorch and Apache MXNet. Its primary objective is to enhance the speed and usability
of distributed deep learning through the implementation of ring-allreduce. This technique necessitates
just a few minimal modifications to the user's code, thereby simplifying the process of distributed deep learning.

## MPI (Message Passing Interface)

The Flyte platform employs the [Kubeflow training operator](https://github.com/kubeflow/training-operator),
to facilitate streamlined execution of all-reduce-style distributed training on Kubernetes.
This integration offers a straightforward interface for conducting distributed training through the utilization of MPI.

The combined power of MPI and Horovod can be harnessed to streamline the complexities of distributed training.
The MPI API serves as a convenient encapsulation to execute Horovod scripts, thereby enhancing the overall efficiency of the process.

## Install the plugin

Install the MPI plugin by running the following command:

```
pip install flytekitplugins-kfmpi
```

## Build a Docker image

The Dockerfile should include installation commands for various components, including MPI and Horovod.

```{literalinclude} ../../../examples/kfmpi_plugin/Dockerfile
:language: docker
:emphasize-lines: 40-51,66
```

## Run the example on the Flyte cluster

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote \
  --image ghcr.io/flyteorg/flytecookbook:kfmpi_plugin-latest \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/kfmpi_plugin/kfmpi_plugin/mpi_mnist.py \
  horovod_training_wf
```

```{auto-examples-toc}
mpi_mnist
```

## MPI Plugin Troubleshooting Guide

This section covers common issues encountered during the setup of the MPI operator for distributed training jobs on Flyte.

**Worker Pods Failing to Start (Insufficient Resources)**

MPI worker pods may fail to start or exhibit scheduling issues, leading to job timeouts or failures. This often occurs due to resource constraints (CPU, memory, or GPU) in the cluster.

1. Adjust Resource Requests:
Ensure that each worker pod has sufficient resources. You can adjust the resource requests in your task definition:

```
    requests=Resources(cpu="<your_cpu_request>", mem="<your_mem_request>")
```

Modify the CPU and memory values according to your cluster's available resources. This helps prevent pod scheduling failures caused by resource constraints.

2. Check Pod Logs for Errors:
If the worker pods still fail to start, check the logs for any related errors:

```
    kubectl logs <pod-name> -n <namespace>
```

Look for resource allocation or worker communication errors.

**Workflow Registration Method Errors (Timeouts or Deadlocks)**

If your MPI workflow hangs or times out, it may be caused by an incorrect workflow registration method.

1. Verify Registration Method:
    When using a custom image, refer to the Flyte documentation on [Registering workflows](https://docs.flyte.org/en/latest/user_guide/flyte_fundamentals/registering_workflows.html#registration-patterns) to ensure you're following the correct registration method.

