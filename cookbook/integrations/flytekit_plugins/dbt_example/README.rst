.. _dbt_integration:

dbt
====

.. tags:: Integration, Data, SQL, Intermediate

`dbt <https://www.getdbt.com/>`__ is one of the widely-used data transformation
tools for working with data directly in a data warehouse. It's optimized for
analytics use cases and can be used for business intelligence, operational
analytics, and even machine learning.

The Flytekit ``dbt`` plugin is a Python module that provides an easy way to
invoke basic ``dbt`` CLI commands from within a Flyte task. The plugin supports
the commands `dbt run <https://docs.getdbt.com/reference/commands/run>`__,
`dbt test <https://docs.getdbt.com/reference/commands/test>`__, and
`dbt source freshness <https://docs.getdbt.com/reference/commands/source>`__.

Prerequisities
--------------

To use the ``dbt`` plugin you'll need to install the ``flytekitplugins-dbt``
plugin.

.. note::

   See `the PyPi page here <https://pypi.org/project/flytekitplugins-dbt/>`__.

.. prompt:: bash $

   pip install flytekitplugins-dbt

Then install dbt itself. You will have to install ``dbt-core`` as well as
the correct adapter for the database that you are accessing.

For example, if you are using a Postgres database you would do:

.. prompt:: bash $

   pip install dbt-postgres

This will install ``dbt-core`` and ``dbt-postgres``, but not any of the other
adapters, ``dbt-redshift``, ``dbt-snowflake``, or ``dbt-bigquery``. See
`the official installation page <https://docs.getdbt.com/docs/get-started/pip-install>`__
for details.


.. _dbt_integration_run:

Running the Example
--------------------

We use a Postgres database installed on the cluster and an example project from
dbt, called `jaffle-shop <https://github.com/dbt-labs/jaffle_shop>`__.
To run the example on your local machine, do the following.

.. important::

   The example below is not designed to run directly in your local
   python environment. It must be run in a Kubernetes cluster, either locally on
   your machine using the ``flytectl demo start`` command or on a cloud cluster.

Start up the demo cluster on your local machine:

.. prompt:: bash $

   flytectl demo start

Pull the pre-built image for this example:

.. prompt:: bash $

   docker pull ghcr.io/flyteorg/flytecookbook:dbt_example-latest
 
This image is built using the following ``Dockerfile`` and contains:

- The ``flytekitplugins-dbt`` and ``dbt-postgres`` Python dependencies.
- The ``jaffle-shop`` example.
- A postgres database.

.. dropdown:: See Dockerfile
   :title: text-muted

   This Dockerfile can be found in the ``flytesnacks/cookbook`` directory under
   the filepath listed in the code block title below.

   .. literalinclude:: ../../../../../integrations/flytekit_plugins/dbt_example/Dockerfile
      :caption: integrations/flytekit_plugins/dbt_example/Dockerfile
      :language: docker
  
To run this example, copy the code in the **dbt example** below into a file
called ``dbt_example.py``, then run it on your local container using the
provided image:

.. prompt:: bash $

   pyflyte run --remote \
       --image ghcr.io/flyteorg/flytecookbook:dbt_example-latest \
       dbt_example.py wf

Alternatively, you can clone the ``flytesnacks`` repo and run the example directly:

.. prompt:: bash $

   git clone https://github.com/flyteorg/flytesnacks
   cd flytesnacks/cookbook/integrations/flytekit_plugins/dbt_example
   pyflyte run --remote \
       --image ghcr.io/flyteorg/flytecookbook:dbt_example-latest \
       dbt_example.py wf
