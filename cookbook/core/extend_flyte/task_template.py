"""
.. _task_tempalate.py:

Writing Task Template Plugins
-----------------------------

The task template-based task execution process differs from the normal function tasks as follows:

    1. The Docker container image is hardcoded into the task definition at serialisation time (by the author of that task type). 
    2. When serialized into a ``TaskTemplate``, the template should contain all of the information required to run that task instance (but not necessarily to reconstitute it).
    3. When Flyte runs the task, the container from #1 is launched. The container should have an executor built into it that understands how to execute the task, solely based on the ``TaskTemplate``.

The following are the key takeaways:

    - The task object that is serialised at compile time does not exist at run time.
    - There is no user function at platform run time, and the executor is responsible for producing outputs based on the task's inputs.

"""
# Other names - task_template/ custom container
# For Flytekit only plugins, you donot need to build a docker image and they are in built. The user need not worry about docker image.
# Examples: sql-alchemy, sqlite