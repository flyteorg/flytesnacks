"""
Running a Workflow
------------------

Workflows on their own are not runnable directly. However, a launchplan is always bound to a workflow and you can use
launchplans to **launch** a workflow. For cases in which you want the launchplan to have the same arguments as a workflow,
if you are using one of the SDK's to author your workflows - like flytekit, flytekit-java etc, then they should
automatically create a ``default launchplan`` for the workflow.

A ``default launchplan`` has the same name as the workflow and all argument defaults are similar. See
:ref:`sphx_glr_auto_remote_access_remote_launchplan.py` to run a workflow via the default launchplan.

:ref:`Tasks also can be executed <sphx_glr_auto_remote_access_run_task.py>` using the launch command.
One difference between running a task and a workflow via launchplans is that launchplans cannot be associated with a
task. This is to avoid triggers and scheduling.

Using flytekit (python):
========================
More details can be found in the docs for  `FlyteRemote <https://docs.flyte.org/projects/flytekit/en/latest/remote.html>`__

.. code-block:: python
    from flytekit.remote import FlyteRemote
    from flytekit.configuration import Config

    # FlyteRemote object is the main entrypoint to API
    remote = FlyteRemote(
        config=Config.for_endpoint(endpoint="flyte.example.net"),
        default_project="flytesnacks",
        default_domain="development",
    )

    # Fetch workflow or launch_plan
    flyte_workflow = remote.fetch_workflow(name="my_workflow", version="v1")
    flyte_launch_plan = remote.fetch_launch_plan(name="my_launch_plan", version="v1")

    # Execute the flyte_entity
    # flyte_entity being either 'flyte_workflow' or 'flyte_launch_plan'
    execution = remote.execute(
        flyte_entity, inputs={...}, execution_name="my_execution", wait=True
    )

"""
