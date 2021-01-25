Kubeflow PyTorch Operator: Native execution on K8s cluster
==========================================================
Pytorch Operator
This section provides examples of how to use Flyte Native Plugins. Native
Plugins are plugins that can be executed without any external service
dependencies. The compute is orchestrated by Flyte itself, within its
provisioned kubernetes clusters


How to build your Dockerfile for Pytorch on K8s
-----------------------------------------------

.. note::

    If using CPU for training then special dockerfile is NOT REQUIRED. If GPU or TPUs are required then, the dockerfile differs only in the driver setup. The following dockerfile is enabled for GPU accelerated training using CUDA

TODO make this the right dockerfile

.. literalinclude:: ../../kfpytorch.Dockerfile
    :language: dockerfile
    :emphasize-lines: 1
    :linenos:
    :caption: Dockerfile for distributed pytorch training is identical to the base dockerfile, except for using CUDA base
