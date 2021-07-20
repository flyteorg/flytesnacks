.. _pytorch-training:

Train a model using pytorch on Flyte
--------------------------------------
Flyte directly has no special understanding of Pytorch. For Flyte, this is just a python library. Where flyte helps is utilizing and bootstrapping the infrastructure
for Pytorch and ensuring that things work well. It also offer the other benefits of using tasks and workflows - checkpointing, separation of concerns and auto-memoization.

Specify GPU requirement
=========================

One of the important directives that is useful when working on deep learning models, is the ability to explicitly request for one or more GPU's. This can done using a simple directive passed to the task declaration as follows,

.. code-block:: python

    from flytekit import Resources, task

    @task(requests=Resources(gpu="1"), limits=Resources(gpu="1"))
    def my_deep_learning_task():
       ...

.. tip:: It is recommended to use the same requests and limits for gpu's as automatic gpu scaling is not supported.

Also to request for GPU's ensure that your Flyte backend has GPU nodes provisioned.

Distributed - data parallel training
=====================================

Flyte also supports distributed training for Pytorch models, but this is not native. This is achieved using one of the optional plugins like,

- Natively on Kubernetes using :ref:`kf-pytorch-op`
- On AWS using :ref:`aws-sagemaker` training

*Other distributed training plugins are coming soon - MPIOperator, Google Vertex AI etc. You can also add your own favourite services*

Example Dockerfile for deployment
==================================
For pytorch if using GPU it is essential, it is necessary to build the dockerfile with GPU support. The examples in this section use a simple nvidia supplied gpu docker image as the base
and the rest of the construction is similar to other files.

.. literalinclude:: ../../../../../case_studies/ml_training/pytorch/Dockerfile

Examples
============
