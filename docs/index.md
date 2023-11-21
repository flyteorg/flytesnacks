---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst

# override the toc-determined page navigation order
next-page: getting_started/getting_started_with_workflow_development
next-page-title: Getting started with workflow development
---

(getting_started_index)=

# About Flyte

Flyte is a workflow orchestrator that seamlessly unifies data engineering, machine learning, and data analytics stacks for building robust and reliable applications. Flyte features:
* Reproducible, repeatable workflows
* Strongly typed interfaces
* Structured datasets to enable easy conversion of dataframes between types, and column-level type checking
* Easy movement of data between local and cloud storage
* Easy tracking of data lineages
* Built-in data and artifact visualization

For a full list of feature, see the [Flyte features page](https://flyte.org/features).

[TK - decide where to put link to hosted sandbox https://sandbox.union.ai/]

## Basic Flyte components

Flyte is made up of a User Plane, Control Plane, and Data Plane.
* The **User Plane** consists of FlyteKit, the FlyteConsole, and Flytectl, which assist in interacting with the core Flyte API. Tasks, workflows, and launch plans are part of the User Plane.
* The **Control Plane** implements the core Flyte API and serves all client requests coming from the User Plane. The Control Plane stores information such as current and past running workflows, and provides that information upon request. It also accepts requests to execute workflows, but offloads the work to the Data Plane.
* The **Data Plane** accepts workflow requests from the Control Plane and guides the workflow to completion, launching tasks on a cluster of machines as necessary based on the workflow graph. The Data Plane sends status events back to the Control Plane so that information can be stored and surfaced to end users.

## Next steps

* To quickly create and run a Flyte workflow, follow the {ref}`Quickstart guide <getting_started_quickstart_guide>`, then read {ref}`"Getting started with workflow development" <getting_started_with_workflow_development>`.
* To create a Flyte Project with lightweight directory structure and configuration files, go to {ref}`"Getting started with workflow development" <getting_started_with_workflow_development>`.

```{toctree}
:maxdepth: 1
:hidden:

|plane| About Flyte <self>
|book-reader| User Guide <userguide>
|chalkboard| Tutorials <tutorials>
|project-diagram| Concepts <https://docs.flyte.org/en/latest/concepts/basics.html>
|rocket| Deployment <https://docs.flyte.org/en/latest/deployment/index.html>
|book| API Reference <https://docs.flyte.org/en/latest/reference/index.html>
|hands-helping| Community <https://docs.flyte.org/en/latest/community/index.html>
```

```{toctree}
:maxdepth: -1
:caption: Getting Started
:hidden:

About Flyte <self>
getting_started/getting_started_with_workflow_development
getting_started/flyte_fundamentals
getting_started/core_use_cases
```

```{toctree}
:maxdepth: -1
:caption: User Guide
:hidden:

📖 User Guide <userguide>
🌳 Environment Setup <environment_setup>
🔤 Basics <auto_examples/basics/index>
⌨️ Data Types and IO <auto_examples/data_types_and_io/index>
🔮 Advanced Composition <auto_examples/advanced_composition/index>
🧩 Customizing Dependencies <auto_examples/customizing_dependencies/index>
🏡 Development Lifecycle <auto_examples/development_lifecycle/index>
⚗️ Testing <auto_examples/testing/index>
🚢 Productionizing <auto_examples/productionizing/index>
🏗 Extending <auto_examples/extending/index>
📝 Contributing <contribute>
```

```{toctree}
:maxdepth: -1
:caption: Tutorials
:hidden:

Tutorials <tutorials>
Model Training <ml_training>
feature_engineering
bioinformatics_examples
flyte_lab
```

```{toctree}
:maxdepth: -1
:caption: Integrations
:hidden:

Integrations <integrations>
auto_examples/airflow_plugin/index
auto_examples/athena_plugin/index
auto_examples/aws_batch_plugin/index
auto_examples/sagemaker_pytorch_plugin/index
auto_examples/sagemaker_training_plugin/index
auto_examples/bigquery_plugin/index
auto_examples/k8s_dask_plugin/index
auto_examples/databricks_plugin/index
auto_examples/dbt_plugin/index
auto_examples/dolt_plugin/index
auto_examples/duckdb_plugin/index
auto_examples/flyin_plugin/index
auto_examples/greatexpectations_plugin/index
auto_examples/hive_plugin/index
auto_examples/k8s_pod_plugin/index
auto_examples/mlflow_plugin/index
auto_examples/mmcloud_plugin/index
auto_examples/modin_plugin/index
auto_examples/kfmpi_plugin/index
auto_examples/onnx_plugin/index
auto_examples/papermill_plugin/index
auto_examples/pandera_plugin/index
auto_examples/kfpytorch_plugin/index
auto_examples/ray_plugin/index
auto_examples/sensor/index
auto_examples/snowflake_plugin/index
auto_examples/k8s_spark_plugin/index
auto_examples/sql_plugin/index
auto_examples/kftensorflow_plugin/index
auto_examples/whylogs_plugin/index
```

```{toctree}
:maxdepth: -1
:caption: Tags
:hidden:

_tags/tagsindex
```
