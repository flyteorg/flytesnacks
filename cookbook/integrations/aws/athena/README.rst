Executing Athena Queries
=======================
Flyte backend can be connected withathena. Once enabled it can allow you to query a athena service (e.g. Qubole) and retrieve typed schema (optionally).
This section will provide how to use the athena Query Plugin using flytekit python

Installation
------------

To use the flytekit athena plugin simply run the following:

.. prompt:: bash

    pip install flytekitplugins-athena

No Need of a dockerfile
------------------------
This plugin is purely a spec and since SQL is completely portable has no need to build a container. Thus this plugin examples do not have any Dockerfile

Configuring the backend to get athena working
-------------------------------------------
.. todo:

This is coming soon.
