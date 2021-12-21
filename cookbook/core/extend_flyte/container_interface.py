"""
.. _core-extend-flyte-container-interface:

Container Interface
-------------------
The Flyte typically interacts with containers in the course of its task execution (since most tasks are container
tasks). If you are extending Flyte with a new container task type, it's worth it to understand how the platform
interacts with containers. This interaction is encoded in two places.

#. At compilation time for a container task, the arguments to that container are set. This is done by flytekit
   for instance for your run of the mill ``@task``.
#. At runtime, Flyte will execute your task via a plugin. The default container plugin (and most other plugins but
   not all) will do the following:
  #. Set a series of environment variables.
  #. Before running the container, the plugin will search/replace values in the container arguments. The
     command templating section below details how this happens.

Command Templating
^^^^^^^^^^^^^^^^^^
The templating of container arguments at run-time is one of the more advanced constructs of Flyte, but one that
authors of new task types should be aware of. For example, when looking at the hello world task in the UI,
if you click the Task tab, you'd see JSON that contains something like the following:

.. code-block:: json

   "container": {
     "command": [],
     "args": [
       "pyflyte-execute",
       "--inputs",
       "{{.input}}",
       "--output-prefix",
       "{{.outputPrefix}}",
       "--raw-output-data-prefix",
       "{{.rawOutputDataPrefix}}",
       "--resolver",
       "flytekit.core.python_auto_container.default_task_resolver",
       "--",
       "task-module",
       "core.basic.hello_world",
       "task-name",
       "say_hello"
     ],

The following table explains what each of the ``{{}}`` items mean, along with some others.

 +--------------------------+-----------------------------+----------------------------------------------------------+
 |       Template           |        Example              |                  Description                             |
 +==========================+=============================+==========================================================+
 |  {{.Input}}              | ``s3://my-bucket/inputs.pb``| Pb file containing a LiteralMap containing the inputs    |
 +--------------------------+-----------------------------+----------------------------------------------------------+
 |  {{.InputPrefix}}        | ``s3://my-bucket``          | Just the bucket where the inputs.pb file can be found    |
 +--------------------------+-----------------------------+----------------------------------------------------------+
 |  {{.Inputs.<xyz>}}       | ``"hello world"``           | For primitive inputs, the task can request that Flyte    |
 |                          |                             | unpack the actual literal value, saving the task from    |
 |                          |                             | having to download the file. Note that for Blob, Schema  |
 |                          |                             | and StructuredDataset types, the uri where the data is   |
 |                          |                             | stored will be filled in as the value.                   |
 +--------------------------+-----------------------------+----------------------------------------------------------+
 |  {{.OutputPrefix}}       | ``s3://my-bucket/abc/data`` | Location where the task should write a LiteralMap of     |
 |                          |                             | output values in a file called ``outputs.pb``            |
 +--------------------------+-----------------------------+----------------------------------------------------------+
 | {{.RawOutputDataPrefix}} | ``s3://your-data/``         | Bucket where off-loaded data types (schemas, files,      |
 |                          |                             | structureddatasets, etc.) are written.                   |
 +--------------------------+-----------------------------+----------------------------------------------------------+
 | {{.PerRetryUniqueKey}}   | (random characters)         | This is a random string that allows the task to          |
 |                          |                             | differentiate between different executions of a task.    |
 |                          |                             | Values will be unique per retry as well.                 |
 +--------------------------+-----------------------------+----------------------------------------------------------+
 | {{.TaskTemplatePath}}    | ``s3://my-bucket/task.pb``  | For tasks that need the full task definition, use this   |
 |                          |                             | template to access the full TaskTemplate IDL message.    |
 |                          |                             | To ensure performance, propeller will not upload this    |
 |                          |                             | file if this template was not requested by the task.     |
 +--------------------------+-----------------------------+----------------------------------------------------------+

"""
