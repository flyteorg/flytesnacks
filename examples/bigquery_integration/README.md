```{eval-rst}
.. tags:: GCP, Data, Integration, Advanced
```

(bigquery_integration)=

# BigQuery integration

You can configure your Flyte deployment to connect to the Google BigQuery service to query BigQuery tables.

There are two implementations of the BigQuery integration:

* **{ref}`BigQuery agent <bigquery_agent>`:** This implementation uses the agents framework (TK - link to agents guide). We strongly recommend using the BigQuery agent rather than the plugin, as agents can be tested locally without running the Flyte backend, are designed to be scalable, can handle large workloads efficiently, and decrease load on FlytePropeller.
* **{ref}`BigQuery plugin <bigquery_plugin>`:** This implementation uses the legacy plugin framework. Only use this documentation if you have already configured your Flyte deployment to use the plugin. If you are using the plugin, we highly recommend migrating to the agent framework version instead, if possible.


```{toctree}
:maxdepth: -1
:hidden:
bigquery_agent
bigquery_plugin
bigquery
```
