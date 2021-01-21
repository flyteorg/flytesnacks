:orphan:



.. _sphx_glr_auto_plugins:

############################################
Flyte Plugins
############################################
Talk about plugins here

What are Flytekit only plugins?
================================


What are Backend Plugins?
=========================


.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_plugins_hive:

Executing Hive Queries
=======================


No Need of a dockerfile?
-------------------------

Configuring the backend to get hive working
-------------------------------------------



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Tasks often start with a data gathering step, and often that data is gathered through Hive. Fly...">

.. only:: html

 .. figure:: /auto_plugins/hive/images/thumb/sphx_glr_hive_thumb.png
     :alt: Write a Hive Task

     :ref:`sphx_glr_auto_plugins_hive_hive.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/hive/hive
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_plugins_sagemaker_training:

AWS Sagemaker Training
=======================
This section provides examples of Flyte Plugins that are designed to work with
AWS Hosted services like Sagemaker, EMR, Athena, Redshift etc

Builtin Algorithms
-------------------

Training a custom model
------------------------



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip=" Defining a XGBoost Training job -------------------------------- We will create a job that wil...">

.. only:: html

 .. figure:: /auto_plugins/sagemaker_training/images/thumb/sphx_glr_sagemaker_builtin_algo_training_thumb.png
     :alt: Training builtin algorithms on Amazon Sagemaker

     :ref:`sphx_glr_auto_plugins_sagemaker_training_sagemaker_builtin_algo_training.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/sagemaker_training/sagemaker_builtin_algo_training

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Custom training algorithms on Amazon Sagemaker">

.. only:: html

 .. figure:: /auto_plugins/sagemaker_training/images/thumb/sphx_glr_sagemaker_custom_training_thumb.png
     :alt: Custom training algorithms on Amazon Sagemaker

     :ref:`sphx_glr_auto_plugins_sagemaker_training_sagemaker_custom_training.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/sagemaker_training/sagemaker_custom_training
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_plugins_k8s_spark:

Executing Spark Jobs natively on K8s Cluster
============================================



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how users can return a spark.Dataset from a task and consume it as a pandas....">

.. only:: html

 .. figure:: /auto_plugins/k8s_spark/images/thumb/sphx_glr_dataframe_passing_thumb.png
     :alt: Pass pandas dataframes

     :ref:`sphx_glr_auto_plugins_k8s_spark_dataframe_passing.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/k8s_spark/dataframe_passing

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how flytekit simplifies usage of pyspark in a users code. The task hello_spa...">

.. only:: html

 .. figure:: /auto_plugins/k8s_spark/images/thumb/sphx_glr_pyspark_pi_thumb.png
     :alt: Creating spark tasks as part of your workflow OR running spark jobs

     :ref:`sphx_glr_auto_plugins_k8s_spark_pyspark_pi.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/k8s_spark/pyspark_pi
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_plugins_kfpytorch:

Kubeflow PyTorch Operator: Native execution on K8s cluster
===========================================================
Pytorch Operator
This section provides examples of how to use Flyte Native Plugins. Native
Plugins are plugins that can be executed without any external service
dependencies. The compute is orchestrated by Flyte itself, within its
provisioned kubernetes clusters



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Running Distributed Pytorch Training using KF PytorchOperator">

.. only:: html

 .. figure:: /auto_plugins/kfpytorch/images/thumb/sphx_glr_pytorch_mnist_thumb.png
     :alt: Running Distributed Pytorch Training using KF PytorchOperator

     :ref:`sphx_glr_auto_plugins_kfpytorch_pytorch_mnist.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/kfpytorch/pytorch_mnist
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_plugins_pod:

Executing K8s Pods
====================



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Pod tasks can be used anytime you need to bring up multiple containers within a single task. Th...">

.. only:: html

 .. figure:: /auto_plugins/pod/images/thumb/sphx_glr_pod_thumb.png
     :alt: Pod plugin example

     :ref:`sphx_glr_auto_plugins_pod_pod.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/pod/pod
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_plugins_sagemaker_pytorch:

AWS Sagemaker distributed training using PyTorch
=================================================



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example is adapted from the following sagemake example. https://github.com/aws/amazon-sage...">

.. only:: html

 .. figure:: /auto_plugins/sagemaker_pytorch/images/thumb/sphx_glr_sagemaker_pytorch_distributed_training_thumb.png
     :alt: DataParallel distributed training of a Pytorch Model on Amazon Sagemaker using Flyte

     :ref:`sphx_glr_auto_plugins_sagemaker_pytorch_sagemaker_pytorch_distributed_training.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_plugins/sagemaker_pytorch/sagemaker_pytorch_distributed_training
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-gallery


  .. container:: sphx-glr-download sphx-glr-download-python

    :download:`Download all examples in Python source code: auto_plugins_python.zip </auto_plugins/auto_plugins_python.zip>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

    :download:`Download all examples in Jupyter notebooks: auto_plugins_jupyter.zip </auto_plugins/auto_plugins_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
