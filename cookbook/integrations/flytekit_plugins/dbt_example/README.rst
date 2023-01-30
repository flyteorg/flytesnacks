dbt
====

.. tags:: Integration, Data, SQL, Intermediate

The Flytekit ``dbt`` plugin is a Python module that provides an easy way to invoke basic ``dbt`` CLI commands from within a Flyte task.
The plugin supports the commands ``dbt run``, ``dbt test``, and ``dbt source freshness``.

Prerequisities
--------------
To use the ``dbt`` plugin you will need to install the following dependencies:

* The plugin, ``flytekitplugins-dbt`` See `the PyPi page here <https://pypi.org/project/flytekitplugins-dbt/>`.

.. code:: bash
  pip install flytekitplugins-dbt

* The dbt tool itself. You will have to install ``dbt-core`` as well as the correct adapter for the database that you are accessing. 
  For example, if you are using a Postgres database you would do

.. code:: bash
  pip install dbt-postgres

This will install ``dbt-core`` and ``dbt-postgres`` (but not any of the other adapters, ``dbt-redshift``, ``dbt-snowflake``, or ``dbt-bigquery``)
See `this page <https://docs.getdbt.com/docs/get-started/pip-install>` for details.


Example
-------

The ``dbt-example`` project below is not designed to run directly in your local python environment. It must be run in a kubernetes cluster, 
either locally on your machine using the Flyte demo cluster solution or on a cloud cluster.

We use a Postgres database installed on the cluster and an example project from dbt, called `jaffle-shop <https://github.com/dbt-labs/jaffle_shop>`).
To run the example on your local machine, do the following.

Start up the demo cluster on your local machine:

.. code:: bash
  flytectl demo start

Pull the pre-built image for this example:

.. code:: bash
  docker pull ghcr.io/flyteorg/flytecookbook:dbt_example-latest
 
This image contains:

* The python dependencies above (``flytekitplugins-dbt``, ``dbt-postgres``).

* The ``jaffle-shop`` example.

* A postgres database.

It is built by this `Dockerfile <https://github.com/flyteorg/flytesnacks/tree/master/cookbook/integrations/flytekit_plugins/dbt_example/Dockerfile>`.
  
Copy the `example code <https://docs.flyte.org/projects/cookbook/en/latest/auto/integrations/flytekit_plugins/dbt_example/dbt_example.html>` into a file called ``dbt_example.py``

Run the example on your local Docker using the provided image:

.. code:: bash
  pyflyte run --remote --image ghcr.io/flyteorg/flytecookbook:dbt_example-latest dbt_example.py wf    
