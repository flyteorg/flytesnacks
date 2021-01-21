:orphan:



.. _sphx_glr_auto_core:

############################################
Examples of using flytekit without plugins
############################################

The intention of this cookbook is to provide a hands on tutorial of various
features in Flyte (specifically if you are using flytekit-python). Flytekit is
intended to be useful even without Flyte backend. All the examples in the
following set are executable locally and we recommend the best way to try out
Flyte is to run these examples locally. The tutorial is divided into 4 sections

``Basic``, ``Intermediate`` & ``Advanced`` sections are laid out in varying levels of difficulty.
``Working with Hosted Flyte Service`` is an independent section and can be used with any of the difficulty
level sections.

Please see additional information in the [GitHub Readme](https://github.com/lyft/flytesnacks/tree/master/cookbook_se) as well.




.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_core_basic:

Basic
=========
This section provides insight into basic building blocks of Flyte, especially flytekit.
Flytekit is a python SDK for developing flyte workflows and task and can be used generally, whenever stateful computation is
desirable. Flytekit developed workflows and tasks are completely runnable locally, unless they need some advanced backend
functionality like, starting a distributed spark cluster.



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to write a task in flytekit python. Recap: In Flyte a task is a fundamen...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_task_thumb.png
     :alt: Tasks

     :ref:`sphx_glr_auto_core_basic_task.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/task

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Once you&#x27;ve had a handle on tasks, we can move to workflows. Workflow are the other basic build...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_basic_workflow_thumb.png
     :alt: Write a simple workflow

     :ref:`sphx_glr_auto_core_basic_basic_workflow.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/basic_workflow

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Launch plans bind a partial or complete list of inputs necessary to launch a workflow along wit...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_lp_thumb.png
     :alt: Launch Plans

     :ref:`sphx_glr_auto_core_basic_lp.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/lp

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Flyte provides the ability to cache the output of task executions in order to make subsequent e...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_task_cache_thumb.png
     :alt: Task Cache

     :ref:`sphx_glr_auto_core_basic_task_cache.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/task_cache

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Files are one of the most fundamental things that users of Python work with, and they are fully...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_files_thumb.png
     :alt: Work with files

     :ref:`sphx_glr_auto_core_basic_files.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/files

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Please also see the entry on files. After files, folders are the other fundamental operating sy...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_folders_thumb.png
     :alt: Work with folders

     :ref:`sphx_glr_auto_core_basic_folders.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/folders

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="A lot of the tasks that you write you can run locally, but some of them you will not be able to...">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_mocking_thumb.png
     :alt: Mock Tasks for Testing

     :ref:`sphx_glr_auto_core_basic_mocking.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/mocking

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="See my workflow as a graph">

.. only:: html

 .. figure:: /auto_core/basic/images/thumb/sphx_glr_graphviz_thumb.png
     :alt: See my workflow as a graph

     :ref:`sphx_glr_auto_core_basic_graphviz.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/basic/graphviz
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_core_intermediate:

Intermediate
=============
Once you have completed the beginner section, the intermediate section provides more intricate examples.
These examples touch more complex features of Flyte - like conditions, dynamic workflows, structured large objects (schemas),
how to leverage extensions like Spark - which allow you to spin up dynamic spark clusters - etc.



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example explains how an untyped schema is passed between tasks using :py:class:`pandas.Dat...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_schema_thumb.png
     :alt: Using Schemas

     :ref:`sphx_glr_auto_core_intermediate_schema.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/schema

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example explains how a typed schema can be used in Flyte and declared in flytekit.">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_typed_schema_thumb.png
     :alt: Typed columns in a schema

     :ref:`sphx_glr_auto_core_intermediate_typed_schema.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/typed_schema

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Launch plans were introduced in the Basics section of this book. Subworkflows are similar in th...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_subworkflows_thumb.png
     :alt: Call another workflow by subworkflow

     :ref:`sphx_glr_auto_core_intermediate_subworkflows.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/subworkflows

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Please make sure you understand the difference between a task and a workflow - feel free to rev...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_dynamics_thumb.png
     :alt: Write a dynamic task

     :ref:`sphx_glr_auto_core_intermediate_dynamics.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/dynamics

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Flyte supports passing JSON&#x27;s between tasks. But, to simplify the usage for the users and intro...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_custom_objects_thumb.png
     :alt: Using custom objects

     :ref:`sphx_glr_auto_core_intermediate_custom_objects.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/custom_objects

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Flytekit supports conditions as a first class construct in the language. Conditions offer a way...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_run_conditions_thumb.png
     :alt: Conditions

     :ref:`sphx_glr_auto_core_intermediate_run_conditions.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/run_conditions

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how it is possible to use arbitrary containers and pass data between them us...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_raw_container_thumb.png
     :alt: Raw container example

     :ref:`sphx_glr_auto_core_intermediate_raw_container.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/raw_container

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Typically when you are working locally, it is preferable to install all requirements of your pr...">

.. only:: html

 .. figure:: /auto_core/intermediate/images/thumb/sphx_glr_multi_images_thumb.png
     :alt: Working with Multiple Container Images in the same workflow

     :ref:`sphx_glr_auto_core_intermediate_multi_images.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/intermediate/multi_images
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_core_advanced:

Advanced
=========
Now that you have seen the capabilities of Flyte and flytekit, you might have found some cases in which you may want to
extend flytekit natively for your own project or better yet contribute to the open source community. This section provides
examples of how flytekit can be easily extended. Flytekit allows 2 fundamental extensions

#. Adding new user space task types. These task types do not need any backend changes and are as simple as writing python
   classes or extending existing python classes to achieve some new functionality.
#. Adding new Types to flytekit's type system. This could enable Flyte to extend its native understanding of more
   complex types or add new types of structured object handling

.. note::

    If you are interested in backend extensions for Flyte - read about it in :any:`working_hosted_service` section.



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="FlyteIdl (the fundamental building block of the Flyte Language) allows various programming lang...">

.. only:: html

 .. figure:: /auto_core/advanced/images/thumb/sphx_glr_run_merge_sort_thumb.png
     :alt: 01: Merge Sort; Conditions & Recursion in Flyte

     :ref:`sphx_glr_auto_core_advanced_run_merge_sort.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/advanced/run_merge_sort

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Flytekit is designed to be extremely extensible. You can add new task-types that are useful onl...">

.. only:: html

 .. figure:: /auto_core/advanced/images/thumb/sphx_glr_custom_task_plugin_thumb.png
     :alt: How to write your own flytekit task plugins?

     :ref:`sphx_glr_auto_core_advanced_custom_task_plugin.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/advanced/custom_task_plugin

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Flyte is a strongly typed framework for authoring tasks and workflows. But, there are situation...">

.. only:: html

 .. figure:: /auto_core/advanced/images/thumb/sphx_glr_run_custom_types_thumb.png
     :alt: How to write/use your custom types in a task?

     :ref:`sphx_glr_auto_core_advanced_run_custom_types.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/advanced/run_custom_types
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_core_remote_flyte:

.. _working_hosted_service:

Working with a Hosted Flyte Service
====================================

Flytekit provides a python SDK for authoring and executing workflows and tasks in python.
Flytekit comes with a simplistic local scheduler that executes code in a local environment.
But, to leverage the full power of Flyte, we recommend using a deployed backend of Flyte. Flyte can be run
on a kubernetes cluster - locally, in a cloud environment or on-prem.

Please refer to the `Installing Flyte <https://lyft.github.io/flyte/administrator/install/index.html>`_ for details on getting started with a Flyte installation.
This section walks through steps on deploying your local workflow to a distributed Flyte environment, with ``NO CODE CHANGES``.


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="One of the reasons why you would want to use a hosted Flyte environment is due to the potential...">

.. only:: html

 .. figure:: /auto_core/remote_flyte/images/thumb/sphx_glr_customizing_resources_thumb.png
     :alt: Customizing task resources like mem/cpu

     :ref:`sphx_glr_auto_core_remote_flyte_customizing_resources.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/remote_flyte/customizing_resources

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="For background on launch plans, refer to launch_plans.">

.. only:: html

 .. figure:: /auto_core/remote_flyte/images/thumb/sphx_glr_lp_schedules_thumb.png
     :alt: Scheduling workflow executions with launch plans

     :ref:`sphx_glr_auto_core_remote_flyte_lp_schedules.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/remote_flyte/lp_schedules

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="For background on launch plans, refer to launch_plans.">

.. only:: html

 .. figure:: /auto_core/remote_flyte/images/thumb/sphx_glr_lp_notifications_thumb.png
     :alt: Getting notifications on workflow termination

     :ref:`sphx_glr_auto_core_remote_flyte_lp_notifications.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_core/remote_flyte/lp_notifications
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-gallery


  .. container:: sphx-glr-download sphx-glr-download-python

    :download:`Download all examples in Python source code: auto_core_python.zip </auto_core/auto_core_python.zip>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

    :download:`Download all examples in Jupyter notebooks: auto_core_jupyter.zip </auto_core/auto_core_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
