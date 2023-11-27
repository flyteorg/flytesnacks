(plugins-snowflake)=

# Snowflake

```{eval-rst}
.. tags:: Integration, Data, Advanced, SQL
```

Flyte can be seamlessly integrated with the [Snowflake](https://www.snowflake.com) service,
providing you with a straightforward means to query data in Snowflake.

## Install the plugin

To use the Snowflake plugin, run the following command:

```
pip install flytekitplugins-snowflake
```

If you intend to run the plugin on the Flyte cluster, you must first set it up on the backend.
Please refer to the
{std:ref}`Snowflake plugin setup guide <flyte:deployment-plugin-setup-webapi-snowflake>`
for detailed instructions.

## Run the example on the Flyte cluster

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/snowflake_plugin/snowflake_plugin/snowflake.py \
  snowflake_wf --nation_key 10
```

```{auto-examples-toc}
snowflake
```
