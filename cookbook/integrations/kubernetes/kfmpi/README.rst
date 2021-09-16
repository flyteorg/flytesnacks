.. _kf-mpi-op:

MPI Operator
=================

This plugin uses the Kubeflow MPI Operator and provides an extremely simplified interface for executing distributed training using MPI.

Installation
------------

To use the flytekit distributed mpi plugin simply run the following:

.. prompt:: bash

   pip install flytekitplugins-kfmpi


How to build your Dockerfile for Pytorch on K8s
-----------------------------------------------

.. note::

    If using CPU for training then special dockerfile is NOT REQUIRED. If GPU or TPUs are required then, the dockerfile differs only in the driver setup. The following dockerfile is enabled for GPU accelerated training using CUDA
    The checked in version of docker file uses python:3.8-slim-buster for faster CI but you can use the Dockerfile pasted below which uses cuda base.
    Additionally the requirements.in uses the cpu version of pytorch. Remove the + cpu for torch and torchvision in requirements.in and make all requirements as shown below

.. prompt:: bash

   make -C integrations/kubernetes/kfmpi requirements
