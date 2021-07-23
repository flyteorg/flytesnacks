Great Expectations
==================

**Great Expectations** is a Python-based open-source library for validating, documenting, and profiling your data. 
It helps to maintain data quality and improve communication about data between teams.

The goodness of data validation in Great Expectations can be integrated with Flyte to validate the data moving in and out of 
the pipeline entities you may have defined in Flyte. This helps establish stricter boundaries around your data to 
ensure that everything's as you expected and that data isn't going to crash your pipelines anymore unexpectedly!

How to Define Your Integration
------------------------------

Great Expectations accepts datasets that can only be "strings" -- file names, table names, etc. 
In Flyte, there are two task types that should suit Great Expectations' "string" hard-and-fast rule apart from the usual "string".

- :py:class:`flytekit.types.file.FlyteFile`: FlyteFile supports remote (and, of course, local) datasets. If a remote URI is given, 
  the plugin downloads data to a user-given file which Great Expectations later validates.
- :py:class:`flytekit.types.schema.FlyteSchema`: FlyteSchema supports tabular data, which the plugin will convert into a parquet file 
  and validate the data using Great Expectations.

In a nutshell, Great Expectations comes in *three modes* in Flyte:

- **Simple String**
- **Flyte Task**: A Flyte task defines the task prototype that one could use within a task or a workflow to validate data using 
  Great Expectations.
- **Flyte Type**: A Flyte type helps attach the ``GreatExpectationsType`` to any dataset.

You'll see all three implementations in the Python code files. 

Plugin Parameters
-----------------

- **data_source**: Data source, in general, is the "name" we use in the config Great Expectations' YAML file. 
  When combined with the data to be validated, this data source helps Great Expectations ascertain the type of data. 
  Moreover, data source also assists in building batches out of data (for validation). 
- **expectation_suite**: Defines the data validation.
- **data_connector**: Tells how the data batches have to be identified.

Optional Parameters
^^^^^^^^^^^^^^^^^^^

- **context_root_dir**: Sets the path of the great expectations config directory. 
- **checkpoint_params**: Optional :py:class:`greatexpectations:great_expectations.checkpoint.checkpoint.SimpleCheckpoint` class parameters.
- **batchrequest_config**: Additional batch request configuration parameters.
  
  - data_connector_query: Query to request a data batch
  - runtime_parameters: Parameters to be sent at run-time
  - batch_identifiers: Batch identifiers
  - batch_spec_passthrough: Reader method if your file doesn’t have an extension
- **local_file_path**: Helpful to download the given dataset to the user-given path.

.. note::
  You may want to mention the **context_root_dir** parameter as providing a path means no harm! 
  Moreover, **local_file_path** is essential when using ``FlyteFile`` and ``FlyteSchema``.

Plugin Installation
-------------------

To use the Great Expectations <> Flyte plugin, run the following command:

.. prompt:: bash $

    pip install flytekitplugins-great_expectations

.. note:: 
    Make sure to run the workflows in the "flytekit_plugins" directory, both locally and within the sandbox.

