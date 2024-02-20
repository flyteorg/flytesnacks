# Databricks

```{eval-rst}
.. tags:: Spark, Integration, DistributedComputing, Data, Advanced
```

Flyte can be integrated with the [Databricks](https://www.databricks.com/) service,
enabling you to submit Spark jobs to the Databricks platform.

There are two implementations of the Databricks integration:

* **{ref}`Databricks agent <databricks_agent>`:** This implementation uses the [agents framework](https://docs.flyte.org/en/latest/flyte_agents/index.html). We strongly recommend using the Databricks agent rather than the plugin, as agents can be tested locally without running the Flyte backend, are designed to be scalable, can handle large workloads efficiently, and decrease load on FlytePropeller.
* **{ref}`Databricks plugin <databricks_plugin>`:** This implementation uses the legacy plugin framework. Only use this documentation if you have already configured your Flyte deployment to use the plugin. If you are using the plugin, we highly recommend migrating to the agent framework version instead, if possible.

```{toctree}
:maxdepth: -1
:hidden:
databricks_agent
databricks_plugin
databricks_job
```
