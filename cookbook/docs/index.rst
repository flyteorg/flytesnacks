User Guide
=========

These tutorials are intended to help the user learn by example. We start with various concepts in flyte and flytekit with examples and
then introduce some of the core plugins. This cookbook is designed to get you running both locally, and on a Flyte cluster using
the `Flytekit Python SDK <https://github.com/lyft/flytekit>`__.

Main Sections
-------------

* :ref:`Core Language Examples <flyte-tutorial>` - This covers the basics of Flytekit, as well as working with a deployed Flyte platform.
* :ref:`Case Studies <sphx_glr_auto_case_studies>` - These are examples that showcase the power of Flyte.
* :ref:`Plugins Examples <plugins_main>` - This section details flytekit extensibility


.. toctree::
   :maxdepth: 4
   :hidden:

   Getting Started <https://docs.flyte.org/en/latest/getting_started.html>
   User Guide <self>
   Concepts <https://docs.flyte.org/en/latest/dive_deep/index.html>
   reference/index
   Community <https://docs.flyte.org/en/latest/community/index.html>

.. toctree::
   :maxdepth: 1
   :caption: Flyte Basics
   :hidden:

   auto_core_flyte_basics/task
   auto_core_flyte_basics/basic_workflow
   auto_core_flyte_basics/imperative_wf_style
   auto_core_flyte_basics/lp
   auto_core_flyte_basics/task_cache
   auto_core_flyte_basics/files
   auto_core_flyte_basics/folders

.. toctree::
   :maxdepth: 1
   :caption: Control Flow
   :hidden:

   auto_core_control_flow/run_conditions
   auto_core_control_flow/subworkflows
   auto_core_control_flow/dynamics
   auto_core_control_flow/map_task
   auto_core_control_flow/run_merge_sort

.. toctree::
   :maxdepth: 1
   :caption: Type System
   :hidden:

   auto_type_system/core
   auto_type_system/schema
   auto_type_system/typed_schema
   auto_type_system/custom_objects

.. toctree::
   :maxdepth: 1
   :caption: Testing
   :hidden:

   auto_testing/mocking

.. toctree::
   :maxdepth: 1
   :caption: Containerization
   :hidden:

   auto_core_containerization/raw_container
   auto_core_containerization/multi_images
   auto_core_containerization/use_secrets
   auto_core_containerization/spot_instances
   auto_core_containerization/workflow_labels_annotations

.. toctree::
   :maxdepth: 4
   :caption: Deployment
   :hidden:

   workflow
   cluster
   guides

.. toctree::
   :maxdepth: 1
   :caption: Control Plane
   :hidden:

   auto_control_plane/register_project
   auto_control_plane/run_task
   auto_control_plane/run_workflow

.. toctree::
   :maxdepth: 4
   :caption: Integrations
   :hidden:

   plugins
   backend_plugins
   flytekit_plugins
   kubernetes
   aws
   gcp
   external_services

.. toctree::
   :maxdepth: 4
   :caption: Extending Flyte
   :hidden:

   auto_core_extend_flyte/introduction
   auto_core_extend_flyte/custom_task_plugin
   auto_core_extend_flyte/run_custom_types
   auto_core_extend_flyte/backend_plugins

.. toctree::
   :maxdepth: 1
   :caption: Tutorials
   :hidden:

   ml_training
   data_processing
   ml_monitoring