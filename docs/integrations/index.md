(integrations)=

# Integrations

Flyte is designed to be highly extensible and can be customized in multiple ways.

```{note}
Want to contribute an integration example? Check out the {ref}`Tutorials and integration examples contribution guide <contribute_examples>`.
```

## Flytekit plugins

Flytekit plugins can be implemented purely in Python, unit tested locally, and allow extending
Flytekit functionality. For comparison, these plugins can be thought of like
[Airflow operators](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/index.html).

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`DBT </auto_examples/dbt_plugin/index>`
  - Run and test your `dbt` pipelines in Flyte.
* - {doc}`Dolt </auto_examples/dolt_plugin/index>`
  - Version your SQL database with `dolt`.
* - {doc}`DuckDB </auto_examples/duckdb_plugin/index>`
  - Run analytical queries using DuckDB.
* - {doc}`Great Expectations </auto_examples/greatexpectations_plugin/index>`
  - Validate data with `great_expectations`.
* - {doc}`MLFlow </auto_examples/mlflow_plugin/index>`
  - `mlflow`: the open standard for model tracking.
* - {doc}`Modin </auto_examples/modin_plugin/index>`
  - Scale pandas workflows with `modin`.
* - {doc}`Neptune </auto_examples/neptune_plugin/index>`
  - `neptune`: Neptune is the MLOps stack component for experiment tracking.
* - {doc}`NIM </auto_examples/nim_plugin/index>`
  - Serve optimized model containers with NIM.
* - {doc}`Ollama </auto_examples/ollama_plugin/index>`
  - Serve fine-tuned LLMs with Ollama in a Flyte workflow.
* - {doc}`ONNX </auto_examples/onnx_plugin/index>`
  - Convert ML models to ONNX models seamlessly.
* - {doc}`Pandera </auto_examples/pandera_plugin/index>`
  - Validate pandas dataframes with `pandera`.
* - {doc}`Papermill </auto_examples/papermill_plugin/index>`
  - Execute Jupyter Notebooks with `papermill`.
* - {doc}`SQL </auto_examples/sql_plugin/index>`
  - Execute SQL queries as tasks.
* - {doc}`Weights and Biases </auto_examples/wandb_plugin/index>`
  - `wandb`: Machine learning platform to build better models faster.
* - {doc}`WhyLogs </auto_examples/whylogs_plugin/index>`
  - `whylogs`: the open standard for data logging.
```

:::{dropdown} {fa}`info-circle` Using Flytekit plugins
:animate: fade-in-slide-down

Data is automatically marshalled and unmarshalled in and out of the plugin. Users should mostly implement the {py:class}`~flytekit.core.base_task.PythonTask` API defined in Flytekit.

Flytekit plugins are lazily loaded and can be released independently like libraries. The naming convention is `flytekitplugins-*`, where `*` indicates the package to be integrated into Flytekit. For example, `flytekitplugins-papermill` enables users to author Flytekit tasks using [Papermill](https://papermill.readthedocs.io/en/latest/).

You can find the plugins maintained by the core Flyte team [here](https://github.com/flyteorg/flytekit/tree/master/plugins).
:::

## Native backend plugins

Native backend plugins can be executed without any external service dependencies because the compute is orchestrated by Flyte itself, within its provisioned Kubernetes clusters.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Kubeflow PyTorch </auto_examples/kfpytorch_plugin/index>`
  - Run distributed PyTorch training jobs using `Kubeflow`.
* - {doc}`Kubeflow TensorFlow </auto_examples/kftensorflow_plugin/index>`
  - Run distributed TensorFlow training jobs using `Kubeflow`.
* - {doc}`Kubernetes pods </auto_examples/k8s_pod_plugin/index>`
  - Execute Kubernetes pods for arbitrary workloads.
* - {doc}`Kubernetes cluster Dask jobs </auto_examples/k8s_dask_plugin/index>`
  - Run Dask jobs on a Kubernetes Cluster.
* - {doc}`Kubernetes cluster Spark jobs </auto_examples/k8s_spark_plugin/index>`
  - Run Spark jobs on a Kubernetes Cluster.
* - {doc}`MPI Operator </auto_examples/kfmpi_plugin/index>`
  - Run distributed deep learning training jobs using Horovod and MPI.
* - {doc}`Ray </auto_examples/ray_plugin/index>`
  - Run Ray jobs on a K8s Cluster.
```

(flyte_agents)=

## Flyte agents

[Flyte agents](https://docs.flyte.org/en/latest/flyte_agents/index.html) are long-running, stateless services that receive execution requests via gRPC and initiate jobs with appropriate external or internal services. Each agent service is a Kubernetes deployment that receives gRPC requests from FlytePropeller when users trigger a particular type of task. (For example, the BigQuery agent handles BigQuery tasks.) The agent service then initiates a job with the appropriate service. If you don't see the agent you need below, see "[Developing agents](https://docs.flyte.org/en/latest/flyte_agents/developing_agents.html)" to learn how to develop a new agent.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`AWS SageMaker Inference agent </auto_examples/sagemaker_inference_agent/index>`
  - Deploy models and create, as well as trigger inference endpoints on AWS SageMaker.
* - {doc}`Airflow agent </auto_examples/airflow_agent/index>`
  - Run Airflow jobs in your workflows with the Airflow agent.
* - {doc}`BigQuery agent </auto_examples/bigquery_agent/index>`
  - Run BigQuery jobs in your workflows with the BigQuery agent.
* - {doc}`ChatGPT agent </auto_examples/chatgpt_agent/index>`
  - Run ChatGPT jobs in your workflows with the ChatGPT agent.
* - {doc}`Databricks agent </auto_examples/databricks_agent/index>`
  - Run Databricks jobs in your workflows with the Databricks agent.
* - {doc}`Memory Machine Cloud agent </auto_examples/mmcloud_agent/index>`
  - Execute tasks using the MemVerge Memory Machine Cloud agent.
* - {doc}`OpenAI Batch </auto_examples/openai_batch_agent/index>`
  - Submit requests for asynchronous batch processing on OpenAI.
* - {doc}`Sensor agent </auto_examples/sensor/index>`
  - Run sensor jobs in your workflows with the sensor agent.
* - {doc}`Snowflake agent </auto_examples/snowflake_agent/index>`
  - Run Snowflake jobs in your workflows with the Snowflake agent.
```

(external_service_backend_plugins)=

## External service backend plugins

As the term suggests, these plugins rely on external services to handle the workload defined in the Flyte task that uses the plugin.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`AWS Athena </auto_examples/athena_plugin/index>`
  - Execute queries using AWS Athena
* - {doc}`AWS Batch </auto_examples/aws_batch_plugin/index>`
  - Running tasks and workflows on AWS batch service
* - {doc}`Flyte Interactive </auto_examples/flyteinteractive_plugin/index>`
  - Execute tasks using Flyte Interactive to debug.
* - {doc}`Hive </auto_examples/hive_plugin/index>`
  - Run Hive jobs in your workflows.
```

(enable-backend-plugins)=

::::{dropdown} {fa}`info-circle` Enabling backend plugins
:animate: fade-in-slide-down

To enable a backend plugin, you must add the `ID` of the plugin to the enabled plugins list. The `enabled-plugins` is available under the `tasks > task-plugins` section of FlytePropeller's configuration.
The plugin configuration structure is defined [here](https://pkg.go.dev/github.com/flyteorg/flytepropeller@v0.6.1/pkg/controller/nodes/task/config#TaskPluginConfig). An example of the config follows:

```yaml
tasks:
  task-plugins:
    enabled-plugins:
      - container
      - sidecar
      - k8s-array
    default-for-task-types:
      container: container
      sidecar: sidecar
      container_array: k8s-array
```

**Finding the `ID` of the backend plugin**

To find the `ID` of the backend plugin, look at the source code of the plugin. For examples, in the case of Spark, the value of `ID` is used [here](https://github.com/flyteorg/flyteplugins/blob/v0.5.25/go/tasks/plugins/k8s/spark/spark.go#L424), defined as [spark](https://github.com/flyteorg/flyteplugins/blob/v0.5.25/go/tasks/plugins/k8s/spark/spark.go#L41).

::::

## SDKs for writing tasks and workflows

The {ref}`community <community>` would love to help you build new SDKs. Currently, the available SDKs are:

```{list-table}
:header-rows: 0
:widths: 20 30

* - [flytekit](https://flytekit.readthedocs.io)
  - The Python SDK for Flyte.
* - [flytekit-java](https://github.com/spotify/flytekit-java)
  - The Java/Scala SDK for Flyte.
```

## Flyte operators

Flyte can be integrated with other orchestrators to help you leverage Flyte's
constructs natively within other orchestration tools.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Airflow </auto_examples/airflow_plugin/index>`
  - Trigger Flyte executions from Airflow.
```

```{toctree}
:maxdepth: -1
:hidden:
:caption: Flytekit plugins

DBT </auto_examples/dbt_plugin/index>
Dolt </auto_examples/dolt_plugin/index>
DuckDB </auto_examples/duckdb_plugin/index>
Great Expectations </auto_examples/greatexpectations_plugin/index>
MLFlow </auto_examples/mlflow_plugin/index>
Modin </auto_examples/modin_plugin/index>
Neptune </auto_examples/neptune_plugin/index>
NIM </auto_examples/nim_plugin/index>
Ollama </auto_examples/ollama_plugin/index>
ONNX </auto_examples/onnx_plugin/index>
Pandera </auto_examples/pandera_plugin/index>
Papermill </auto_examples/papermill_plugin/index>
SQL </auto_examples/sql_plugin/index>
Weights & Biases </auto_examples/wandb_plugin/index>
WhyLogs </auto_examples/whylogs_plugin/index>
```

```{toctree}
:maxdepth: -1
:hidden:
:caption: Native backend plugins

Kubeflow PyTorch </auto_examples/kfpytorch_plugin/index>
Kubeflow TensorFlow </auto_examples/kftensorflow_plugin/index>
Kubernetes cluster Dask jobs </auto_examples/k8s_dask_plugin/index>
Kubernetes cluster Spark jobs </auto_examples/k8s_spark_plugin/index>
MPI Operator </auto_examples/kfmpi_plugin/index>
Ray </auto_examples/ray_plugin/index>
```

```{toctree}
:maxdepth: -1
:hidden:
:caption: Flyte agents

Airflow agent </auto_examples/airflow_agent/index>
AWS Sagemaker inference agent </auto_examples/sagemaker_inference_agent/index>
BigQuery agent </auto_examples/bigquery_agent/index>
ChatGPT agent </auto_examples/chatgpt_agent/index>
Databricks agent </auto_examples/databricks_agent/index>
Memory Machine Cloud agent </auto_examples/mmcloud_agent/index>
OpenAI batch agent </auto_examples/openai_batch_agent/index>
Sensor agent </auto_examples/sensor/index>
Snowflake agent </auto_examples/snowflake_agent/index>
```

```{toctree}
:maxdepth: -1
:hidden:
:caption: External service backend plugins

AWS Athena </auto_examples/athena_plugin/index>
AWS Batch </auto_examples/aws_batch_plugin/index>
Flyte Interactive </auto_examples/flyteinteractive_plugin/index>
Hive </auto_examples/hive_plugin/index>

```

```{toctree}
:maxdepth: -1
:hidden:
:caption: SDKs for writing tasks and workflows

flytekit <https://flytekit.readthedocs.io/>
flytekit-java <https://github.com/spotify/flytekit-java>

```

```{toctree}
:maxdepth: -1
:hidden:
:caption: Flyte operators

Airflow </auto_examples/airflow_plugin/index>
```

```{toctree}
:maxdepth: -1
:hidden:
:caption: Deprecated integrations

BigQuery plugin </auto_examples/bigquery_plugin/index>
Databricks plugin </auto_examples/databricks_plugin/index>
Kubernetes pods </auto_examples/k8s_pod_plugin/index>
Snowflake plugin </auto_examples/snowflake_plugin/index>
```
