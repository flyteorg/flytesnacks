Snowflake
====

Flyte backend can be connected with snowflake service. Once enabled it can allow you to query a snowflake service and retrieve typed schema (optionally).
This section will provide how to use the Snowflake Query Plugin using flytekit python

Installation
------------

To use the flytekit snowflake plugin simply run the following:

.. prompt:: bash

    pip install flytekitplugins-snowflake

No Need of a dockerfile
------------------------
This plugin is purely a spec. Since SQL is completely portable there is no need to build a Docker container.


Configuring the backend to get snowflake working
---------------------------------------------
1. Make sure to add "snowflake" in ``tasks.task-plugins.enabled-plugin`` in `enabled_plugins.yaml <https://github.com/flyteorg/flyte/blob/master/deployment/sandbox/flyte_generated.yaml#L2296>`_

2. Add snowflake JWT token to Flytepropeller. `here <https://docs.snowflake.com/en/developer-guide/sql-api/guide.html#using-key-pair-authentication>`_ to see more detail to setup snowflake JWT token.

    ``kubectl set env deployment/flytepropeller FLYTE_SECRET_FLYTE_SNOWFLAKE_CLIENT_TOKEN=<jwt_token> -n flyte``
