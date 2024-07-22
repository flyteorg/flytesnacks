---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst

# override the toc-determined page navigation order
next-page: getting_started/quickstart_guide
next-page-title: Quickstart guide
---

(getting_started_index)=

# Introduction to Flyte

Flyte is a workflow orchestrator that unifies machine learning, data engineering, and data analytics stacks for building robust and reliable applications. Flyte features:

- Reproducible, repeatable workflows
- Strongly typed interfaces
- Structured datasets to enable easy conversion of dataframes between types, and column-level type checking
- Easy movement of data between local and cloud storage
- Easy tracking of data lineages
- Built-in data and artifact visualization

For a full list of feature, see the [Flyte features page](https://flyte.org/features).

## Basic Flyte components

Flyte is made up of a user plane, control plane, and data plane.

- The **user plane** contains the elements you need to develop the code that will implement your application's directed acyclic graph (DAG). These elements are FlyteKit and Flytectl. Data scientists and machine learning engineers primarily work in the user plane.
- The **control plane** is part of the Flyte backend that is configured by platform engineers or others tasked with setting up computing infrastructure. It consists of FlyteConsole and FlyteAdmin, which serves as the main Flyte API to process requests from clients in the user plane. The control plane sends workflow execution requests to the data plane for execution, and stores information such as current and past running workflows, and provides that information upon request.
- The **data plane** is another part of the Flyte backend that contains FlytePropeller, the core engine of Flyte that executes workflows. FlytePropeller is designed as a [Kubernetes Controller](https://kubernetes.io/docs/concepts/architecture/controller/). The data plane sends status events back to the control plane so that information can be stored and surfaced to end users.

## Next steps

- To quickly try out Flyte on your machine, follow the {ref}`Quickstart guide <getting_started_quickstart_guide>`.
- To create a Flyte project that can be used to package workflow code for deployment to a Flyte cluster, see {ref}`"Getting started with workflow development" <getting_started_workflow_development>`.
- To set up a Flyte cluster, see the [Deployment documentation](https://docs.flyte.org/en/latest/deployment/index.html).

```{toctree}
:maxdepth: 1
:hidden:

Getting Started <self>
User Guide <https://docs.flyte.org/en/latest/user_guide/index.html>
Tutorials <tutorials>
Concepts <https://docs.flyte.org/en/latest/concepts/basics.html>
Deployment <https://docs.flyte.org/en/latest/deployment/index.html>
API Reference <https://docs.flyte.org/en/latest/reference/index.html>
Community <https://docs.flyte.org/en/latest/community/index.html>
```

```{toctree}
:maxdepth: -1
:caption: Getting Started
:hidden:

Introduction to Flyte <self>
Quickstart guide <https://docs.flyte.org/en/latest/quickstart_guide.html>
Getting started with workflow development <https://docs.flyte.org/en/latest/getting_started_with_workflow_development/index.html>
Flyte fundamentals <https://docs.flyte.org/en/latest/flyte_fundamentals/index.html>
Core use cases <https://docs.flyte.org/en/latest/core_use_cases/index.html>
```

```{toctree}
:maxdepth: -1
:caption: User Guide
:hidden:

📖 User Guide <https://docs.flyte.org/en/latest/user_guide/index.html>
🌳 Environment Setup <https://docs.flyte.org/en/latest/user_guide/environment_setup.html>
🔤 Basics <https://docs.flyte.org/en/latest/user_guide/basics/index.html>
⌨️ Data Types and IO <https://docs.flyte.org/en/latest/user_guide/data_types_and_io/index.html>
🔮 Advanced Composition <https://docs.flyte.org/en/latest/user_guide/advanced_composition/index.html>
🧩 Customizing Dependencies <https://docs.flyte.org/en/latest/user_guide/customizing_dependencies/index.html>
🏡 Development Lifecycle <https://docs.flyte.org/en/latest/user_guide/development_lifecycle/index.html>
⚗️ Testing <https://docs.flyte.org/en/latest/user_guide/testing/index.html>
🚢 Productionizing <https://docs.flyte.org/en/latest/user_guide/productionizing/index.html>
🏗 Extending <https://docs.flyte.org/en/latest/user_guide/extending/index.html>
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
auto_examples/airflow_agent/index
auto_examples/airflow_plugin/index
auto_examples/athena_plugin/index
auto_examples/aws_batch_plugin/index
auto_examples/bigquery_agent/index
auto_examples/chatgpt_agent/index
auto_examples/k8s_dask_plugin/index
auto_examples/databricks_agent/index
auto_examples/dbt_plugin/index
auto_examples/dolt_plugin/index
auto_examples/duckdb_plugin/index
auto_examples/flyteinteractive_plugin/index
auto_examples/greatexpectations_plugin/index
auto_examples/hive_plugin/index
auto_examples/k8s_pod_plugin/index
auto_examples/mlflow_plugin/index
auto_examples/mmcloud_agent/index
auto_examples/modin_plugin/index
auto_examples/kfmpi_plugin/index
auto_examples/nim_wrapper/index
auto_examples/onnx_plugin/index
auto_examples/openai_batch_agent/index
auto_examples/papermill_plugin/index
auto_examples/pandera_plugin/index
auto_examples/kfpytorch_plugin/index
auto_examples/ray_plugin/index
auto_examples/sagemaker_inference_agent/index
auto_examples/sensor/index
auto_examples/snowflake_agent/index
auto_examples/k8s_spark_plugin/index
auto_examples/sql_plugin/index
auto_examples/kftensorflow_plugin/index
auto_examples/whylogs_plugin/index
```

```{toctree}
:maxdepth: -1
:caption: Deprecated integrations
:hidden:

Deprecated integrations <https://docs.flyte.org/en/latest/deprecated_integrations/index.html>
BigQuery plugin <https://docs.flyte.org/en/latest/deprecated_integrations/bigquery_plugin/index.html>
Databricks plugin <https://docs.flyte.org/en/latest/deprecated_integrations/databricks_plugin/index.html>
Snowflake plugin <https://docs.flyte.org/en/latest/deprecated_integrations/snowflake_plugin/index.html>
```

```{toctree}
:maxdepth: -1
:caption: Tags
:hidden:

_tags/tagsindex
```
