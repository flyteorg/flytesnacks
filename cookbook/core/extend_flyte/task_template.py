"""
.. _task_tempalate.py:

Writing Task Template Plugins
-----------------------------

Task Templates are useful as they: 
 - Shift the burden of writing Dockerfile from the user who uses the task in workflows, to the author of the task type.
 - Allow the author to optimize the image that the task runs on.
 - Make it possible to (largely) extend the Flyte task execution behavior without using backend golang plugin. 
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

"""
# Other names - task_template/ custom container
# For Flytekit only plugins, you donot need to build a docker image and they are in built. The user need not worry about docker image.
# Examples: sql-alchemy, sqlite