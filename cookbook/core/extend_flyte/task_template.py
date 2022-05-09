"""
.. _task_tempalate.py:

Writing Task Template Plugins
-----------------------------

Task Templates are useful as they: 
 - Shift the burden of writing Dockerfile from the user who uses the task in workflows to the author of the task type.
 - Allow the author to optimize the image that the task runs on.
 - Make it possible to (largely) extend the Flyte task execution behavior without using the backend GOlang plugin. 
   The caveat is that these tasks can't access the K8s cluster, so you'll still need a backend plugin if you want a custom task type that generates CRD.  

The task template-based task execution process differs from the normal function tasks as follows:
 1. The Docker container image is hardcoded into the task definition at serialization time (by the author of that task type). 
 2. When serialized into a ``TaskTemplate``, the template should contain all of the information required to run that task instance (but not necessarily to reconstitute it).
 3. When Flyte runs the task, the container from #1 is launched. The container should have an executor built into it that understands how to execute the task, solely based on the ``TaskTemplate``.

The following are the key takeaways:
 - The task object serialized at compile time does not exist at run time.
 - There is no user function at platform run time, and the executor is responsible for producing outputs based on the task's inputs.

Using a Task
*************

Take a look at the `example PR <https://github.com/flyteorg/flytekit/pull/470>`__, where we switched the built-in SQLite3 task from the old to the new style of writing tasks.

There aren't many changes from the user's standpoint:
 - Install whichever Python library has the task type definition (in the case of SQLite3, it's bundled in Flytekit, but this isn't always the case). 
 - Import and instantiate the task as you would for any other type of non-function-based task.

How to write a Task
********************

Writing one of the new tasks consists of three steps.

The task extension code consists of two classes: 
 1. Task class
 2. Executor class
 3. A Dockerfile that is executed when any user runs your task. It'll most likely include Flytekit, Python, and your task extension code. 

To follow along with the below, use the `PR (mentioned above) <https://github.com/flyteorg/flytekit/pull/470>`__ where we migrate the SQLite3 task. 

Python Library
**************

Task
====
New tasks of this type must be created as a subclass of the ``PythonCustomizedContainerTask`` class. 

Specifically, you'll need to customize these three arguments to the parent class constructor:
 * ``container_image`` This is the container image that will run on a Flyte platform when the user invokes the job.
 * ``executor_type`` This should be the Python class that inherits the ``ShimTaskExecutor``.
 * ``task_type`` All types have a task type. Flyte engine uses this string to identify which plugin to use when running a task. 
The container plugin will be used for everything that doesn't have an explicit match (which is correct in this case). So you may call it whatever you want, just not something that's already been claimed  (like "spark" or something).

Referring to the SQLite3 example ::

    container_image="ghcr.io/flyteorg/flytekit-py37:v0.18.1",
    executor_type=SQLite3TaskExecutor,
    task_type="sqlite3",

Note that the container is special in this case since the Python classes' definitions are included in Flytekit; we utilize the Flytekit image.

Furthermore, you need to override the ``get_custom`` function.  Keep in mind that the task's execution behavior is entirely defined by the task's serialized form (that is, the serialized ``TaskTemplate``). 
This function stores and inserts the data into the template's `custom field <https://github.com/flyteorg/flyteidl/blob/7302971c064b6061a148f2bee79f673bc8cf30ee/protos/flyteidl/core/tasks.proto#L114>`__. However, keep the task template's overall size to a minimum.

Executor
========
You must subclass and override the ``execute_from_model`` function for the ``ShimTaskExecutor`` abstract class. This function will be invoked in both local workflow execution and platform-run-time execution, and it will include all of the business logic of your task.

The signature of this execute function differs from the ``execute`` functions of most other tasks since the ``TaskTemplate`` determines all the business logic, including how the task is run.

Image
=======
This is the custom image that you specified in the subclass ``PythonCustomizedContainerTask``. Out of the box, when Flyte runs the container, these tasks will run a command that looks like this ::

    pyflyte-execute --inputs s3://inputs.pb --output-prefix s3://outputs --raw-output-data-prefix s3://user-data --resolver flytekit.core.python_customized_container_task.default_task_template_resolver -- {{.taskTemplatePath}} path.to.your.executor.subclass

This means that your `Docker image <https://github.com/flyteorg/flytekit/blob/master/Dockerfile.py3.10>`_ will need Python and Flytekit installed. The container's Python interpreter should be able to find your custom executor class at the import path ``path.to.your.executor.subclass``.

"""
