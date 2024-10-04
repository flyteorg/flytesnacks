(integrations)=

# Integrations

Flyte is designed to be highly extensible and can be customized in multiple ways.

```{note}
Want to contribute an example? Check out the {doc}`Example Contribution Guide <contribute>`.
```

## Flytekit Plugins

Flytekit plugins are simple plugins that can be implemented purely in python, unit tested locally and allow extending
Flytekit functionality. These plugins can be anything and for comparison can be thought of like
[Airflow Operators](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/index.html).

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`SQL <auto_examples/sql_plugin/index>`
  - Execute SQL queries as tasks.
* - {doc}`Great Expectations <auto_examples/greatexpectations_plugin/index>`
  - Validate data with `great_expectations`.
* - {doc}`Papermill <auto_examples/papermill_plugin/index>`
  - Execute Jupyter Notebooks with `papermill`.
* - {doc}`Pandera <auto_examples/pandera_plugin/index>`
  - Validate pandas dataframes with `pandera`.
* - {doc}`Modin <auto_examples/modin_plugin/index>`
  - Scale pandas workflows with `modin`.
* - {doc}`Dolt <auto_examples/dolt_plugin/index>`
  - Version your SQL database with `dolt`.
* - {doc}`DBT <auto_examples/dbt_plugin/index>`
  - Run and test your `dbt` pipelines in Flyte.
* - {doc}`WhyLogs <auto_examples/whylogs_plugin/index>`
  - `whylogs`: the open standard for data logging.
* - {doc}`MLFlow <auto_examples/mlflow_plugin/index>`
  - `mlflow`: the open standard for model tracking.
* - {doc}`ONNX <auto_examples/onnx_plugin/index>`
  - Convert ML models to ONNX models seamlessly.
* - {doc}`DuckDB <auto_examples/duckdb_plugin/index>`
  - Run analytical queries using DuckDB.
* - {doc}`Weights and Biases <auto_examples/wandb_plugin/index>`
  - `wandb`: Machine learning platform to build better models faster.
* - {doc}`Neptune <auto_examples/neptune_plugin/index>`
  - `neptune`: Neptune is the MLOps stack component for experiment tracking.
* - {doc}`NIM <auto_examples/nim_plugin/index>`
  - Serve optimized model containers with NIM.
* - {doc}`Ollama <auto_examples/ollama_plugin/index>`
  - Serve fine-tuned LLMs with Ollama in a Flyte workflow.
```

:::{dropdown} {fa}`info-circle` Using flytekit plugins
:animate: fade-in-slide-down

Data is automatically marshalled and unmarshalled in and out of the plugin. Users should mostly implement the
{py:class}`~flytekit.core.base_task.PythonTask` API defined in Flytekit.

Flytekit Plugins are lazily loaded and can be released independently like libraries. We follow a convention to name the
plugin like `flytekitplugins-*`, where `*` indicates the package to be integrated into Flytekit. For example
`flytekitplugins-papermill` enables users to author Flytekit tasks using [Papermill](https://papermill.readthedocs.io/en/latest/).

You can find the plugins maintained by the core Flyte team [here](https://github.com/flyteorg/flytekit/tree/master/plugins).
:::

## Native Backend Plugins

Native Backend Plugins are the plugins that can be executed without any external service dependencies because the compute is
orchestrated by Flyte itself, within its provisioned Kubernetes clusters.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`K8s Pods <auto_examples/k8s_pod_plugin/index>`
  - Execute K8s pods for arbitrary workloads.
* - {doc}`K8s Cluster Dask Jobs <auto_examples/k8s_dask_plugin/index>`
  - Run Dask jobs on a K8s Cluster.
* - {doc}`K8s Cluster Spark Jobs <auto_examples/k8s_spark_plugin/index>`
  - Run Spark jobs on a K8s Cluster.
* - {doc}`Kubeflow PyTorch <auto_examples/kfpytorch_plugin/index>`
  - Run distributed PyTorch training jobs using `Kubeflow`.
* - {doc}`Kubeflow TensorFlow <auto_examples/kftensorflow_plugin/index>`
  - Run distributed TensorFlow training jobs using `Kubeflow`.
* - {doc}`MPI Operator <auto_examples/kfmpi_plugin/index>`
  - Run distributed deep learning training jobs using Horovod and MPI.
* - {doc}`Ray Task <auto_examples/ray_plugin/index>`
  - Run Ray jobs on a K8s Cluster.
```

(flyte_agents)=

## Flyte agents

[Flyte agents](https://docs.flyte.org/en/latest/flyte_agents/index.html) are long-running, stateless services that receive execution requests via gRPC and initiate jobs with appropriate external or internal services. Each agent service is a Kubernetes deployment that receives gRPC requests from FlytePropeller when users trigger a particular type of task. (For example, the BigQuery agent handles BigQuery tasks.) The agent service then initiates a job with the appropriate service. If you don't see the agent you need below, see "[Developing agents](https://docs.flyte.org/en/latest/flyte_agents/developing_agents.html)" to learn how to develop a new agent.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Airflow agent <auto_examples/airflow_agent/index>`
  - Run Airflow jobs in your workflows with the Airflow agent.
* - {doc}`BigQuery agent <auto_examples/bigquery_agent/index>`
  - Run BigQuery jobs in your workflows with the BigQuery agent.
* - {doc}`ChatGPT agent <auto_examples/chatgpt_agent/index>`
  - Run ChatGPT jobs in your workflows with the ChatGPT agent.
* - {doc}`Databricks <auto_examples/databricks_agent/index>`
  - Run Databricks jobs in your workflows with the Databricks agent.
* - {doc}`Memory Machine Cloud <auto_examples/mmcloud_agent/index>`
  - Execute tasks using the MemVerge Memory Machine Cloud agent.
* - {doc}`OpenAI Batch <auto_examples/openai_batch_agent/index>`
  - Submit requests for asynchronous batch processing on OpenAI.
* - {doc}`SageMaker Inference <auto_examples/sagemaker_inference_agent/index>`
  - Deploy models and create, as well as trigger inference endpoints on SageMaker.
* - {doc}`Sensor <auto_examples/sensor/index>`
  - Run sensor jobs in your workflows with the sensor agent.
* - {doc}`Snowflake <auto_examples/snowflake_agent/index>`
  - Run Snowflake jobs in your workflows with the Snowflake agent.
```

(external_service_backend_plugins)=

## External Service Backend Plugins

As the term suggests, external service backend plugins rely on external services like
[Hive](https://docs.qubole.com/en/latest/user-guide/engines/hive/index.html) for handling the workload defined in the Flyte task that uses the respective plugin.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`AWS Athena plugin <auto_examples/athena_plugin/index>`
  - Execute queries using AWS Athena
* - {doc}`AWS Batch plugin <auto_examples/aws_batch_plugin/index>`
  - Running tasks and workflows on AWS batch service
* - {doc}`Flyte Interactive <auto_examples/flyteinteractive_plugin/index>`
  - Execute tasks using Flyte Interactive to debug.
* - {doc}`Hive plugin <auto_examples/hive_plugin/index>`
  - Run Hive jobs in your workflows.
```

(enable-backend-plugins)=

::::{dropdown} {fa}`info-circle` Enabling Backend Plugins
:animate: fade-in-slide-down

To enable a backend plugin you have to add the `ID` of the plugin to the enabled plugins list. The `enabled-plugins` is available under the `tasks > task-plugins` section of FlytePropeller's configuration.
The plugin configuration structure is defined [here](https://pkg.go.dev/github.com/flyteorg/flytepropeller@v0.6.1/pkg/controller/nodes/task/config#TaskPluginConfig). An example of the config follows,

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

**Finding the `ID` of the Backend Plugin**

This is a little tricky since you have to look at the source code of the plugin to figure out the `ID`. In the case of Spark, for example, the value of `ID` is used [here](https://github.com/flyteorg/flyteplugins/blob/v0.5.25/go/tasks/plugins/k8s/spark/spark.go#L424) here, defined as [spark](https://github.com/flyteorg/flyteplugins/blob/v0.5.25/go/tasks/plugins/k8s/spark/spark.go#L41).

::::

## SDKs for Writing Tasks and Workflows

The {ref}`community <community>` would love to help you with your own ideas of building a new SDK. Currently the available SDKs are:

```{list-table}
:header-rows: 0
:widths: 20 30

* - [flytekit](https://flytekit.readthedocs.io)
  - The Python SDK for Flyte.
* - [flytekit-java](https://github.com/spotify/flytekit-java)
  - The Java/Scala SDK for Flyte.
```

## Flyte Operators

Flyte can be integrated with other orchestrators to help you leverage Flyte's
constructs natively within other orchestration tools.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Airflow <auto_examples/airflow_plugin/index>`
  - Trigger Flyte executions from Airflow.
```
