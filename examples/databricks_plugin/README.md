# Databricks

```{eval-rst}
.. tags:: Spark, Integration, DistributedComputing, Data, Advanced
```

Flyte can be seamlessly integrated with the [Databricks](https://www.databricks.com/) service,
enabling you to effortlessly submit Spark jobs to the Databricks platform.

## Local usage

### Install the plugin

The Databricks plugin comes bundled with the Spark plugin.
To execute it locally, run the following command:

```
pip install flytekitplugins-spark
```

### Run code locally

For example code you can run locally, see {doc}`"Running Spark on Databricks" <databricks_job>`

## Flyte cluster usage

If you intend to run the plugin on the Flyte cluster, you must first set it up on the backend.
Please refer to the
{std:ref}`Databricks plugin setup guide <flyte:deployment-plugin-setup-webapi-databricks>`
for detailed instructions.

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote \
  --image ghcr.io/flyteorg/flytecookbook:databricks_plugin-latest \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/databricks_plugin/databricks_plugin/databricks_job.py \
  my_databricks_job
```

:::{note}
Using Spark on Databricks is incredibly simple and offers comprehensive versioning through a
custom-built Spark container. This built container also facilitates the execution of standard Spark tasks.

To utilize Spark, the image should employ a base image provided by Databricks,
and the workflow code must be copied to `/databricks/driver`.

```{literalinclude} ../../../examples/databricks_plugin/Dockerfile
:language: docker
:emphasize-lines: 1,7-8,20
```

```{toctree}
:hidden:

databricks_job
```
