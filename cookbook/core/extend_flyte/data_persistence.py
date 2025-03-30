"""
.. _extend-flyte-persistence-plugin:

##########################
Writing Custom Persistence Plugin
##########################

Currently, flytekit uses `awscli <https://aws.amazon.com/cli/>`__ or `gcsutil <https://cloud.google.com/storage/docs/gsutil>`__
by default to download the task's input and upload the task's output from the blob store. You may, however, want to write data to another storage service, such as HDFS or FTP. Flytekit provides a flexible way to extend and register a new persistence plugin.

Let us try to recap, why we should implement a persistence plugin

- Speed up blob store operations.
- Download the task input from a file system that Flyte doesn't support.
- You have a custom authentication workflow in your own SDK

Add Custom Persistence Plugin
=============================
1. Extend `DataPersistence <https://docs.flyte.org/projects/flytekit/en/latest/generated/flytekit.extend.DataPersistence.html#flytekit-extend-datapersistence>`__ and implement the interface.
2. Register it to the `DataPersistencePlugins <https://docs.flyte.org/projects/flytekit/en/latest/generated/flytekit.extend.DataPersistencePlugins.html#flytekit-extend-datapersistenceplugins>`__ or overwrite the existing persistence plugin.

Example
=======
Implement all the abstract functions in ``DataPersistence`` so that flytekit will know how to access and connect to your file systems.

.. code-block:: python

    class CustomPersistence(DataPersistence)::

        def __init__(self, name: str, default_prefix: typing.Optional[str] = None, **kwargs):
            self._name = name
            self._default_prefix = default_prefix

            @property
            def name(self) -> str:
                return self._name

            @property
            def default_prefix(self) -> typing.Optional[str]:
                return self._default_prefix

            def listdir(self, path: str, recursive: bool = False) -> typing.Generator[str, None, None]:
                 # Returns true if the given path exists, else false
                raise UnsupportedPersistenceOp(f"Listing a directory is not supported by the persistence plugin {self.name}")

           def exists(self, path: str) -> bool:
                # Returns true if the given path exists, else false
                pass

           def get(self, from_path: str, to_path: str, recursive: bool = False):
                # Retrieves data from from_path and writes to the given to_path (to_path is locally accessible)
                pass

           def put(self, from_path: str, to_path: str, recursive: bool = False):
                # Stores data from from_path and writes to the given to_path (from_path is locally accessible)
                pass

           def construct_path(self, add_protocol: bool, add_prefix: bool, *paths: str) -> str:
                # if add_protocol is true then <protocol> is prefixed else
                # Constructs a path in the format <base><delim>*args
                # delim is dependent on the storage medium.
                # each of the args is joined with the delim
                pass

    DataPersistencePlugins.register_plugin("cf://", CustomPersistence)


Here is also an `example <https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-data-fsspec/flytekitplugins/fsspec/persist.py>`__
of adding a custom plugin by leveraging fsspec. Flytekit will use fsspec to do blob operation by default if the ``flytekit-data-fsspec`` plugin is installed.

"""