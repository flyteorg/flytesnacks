(snowflake_integration)=
# Snowflake

```{eval-rst}
.. tags:: AWS, GCP, AliCloud, Integration, Advanced
```
Flyte can be seamlessly integrated with the [Snowflake](https://www.snowflake.com) service,
providing you with a straightforward means to query data in Snowflake.

There are two implementations of the Snowflake integration:

* **{ref}`Snowflake agent <snowflake_agent>`:** This implementation uses the [agents framework](https://docs.flyte.org/en/latest/flyte_agents/index.html). We strongly recommend using the Snowflake agent rather than the plugin, as agents can be tested locally without running the Flyte backend, are designed to be scalable, can handle large workloads efficiently, and decrease load on FlytePropeller.
* **{ref}`Snowflake plugin <snowflake_plugin>`:** This implementation uses the legacy plugin framework. Only use this documentation if you have already configured your Flyte deployment to use the plugin. If you are using the plugin, we highly recommend migrating to the agent framework version instead, if possible.

```{toctree}
:maxdepth: -1
:hidden:

snowflake_agent
snowflake_plugin
snowflake
```
