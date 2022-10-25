"""
Running a Launchplan
--------------------

Flytectl:
=============

This is multi-steps process where we create an execution spec file, update the spec file and then create the execution.
More details can be found `here <https://docs.flyte.org/projects/flytectl/en/stable/gen/flytectl_create_execution.html>`__.

**Generate an execution spec file** ::

    flytectl get launchplan -p flytesnacks -d development myapp.workflows.example.my_wf  --execFile exec_spec.yaml

**Update the input spec file for arguments to the workflow** ::

    ....
    inputs:
        name: "adam"
    ....

**Create execution using the exec spec file** ::

    flytectl create execution -p flytesnacks -d development --execFile exec_spec.yaml


**Monitor the execution by providing the execution id from create command** ::

    flytectl get execution -p flytesnacks -d development <execid>

FlyteRemote:
========================

More details can be found in the docs for  `FlyteRemote <https://docs.flyte.org/projects/flytekit/en/latest/remote.html>`__

.. code-block:: python

    from flytekit.remote import FlyteRemote
    from flytekit.configuration import Config
    from flytekit import LaunchPlan

    # FlyteRemote object is the main entrypoint to API
    remote = FlyteRemote(
        config=Config.for_endpoint(endpoint="flyte.example.net"),
        default_project="flytesnacks",
        default_domain="development",
    )

    # Fetch workflow
    flyte_workflow = remote.fetch_workflow(
        name="workflows.statistics_flow", version="v1", project="flytesnacks", domain="development"
    )

    # Get or create attached launchplan
    flyte_launch_plan = LaunchPlan.get_or_create(name="workflows.statistics_plan", workflow=flyte_workflow)

    # Execute
    execution = remote.execute(
        flyte_launch_plan, inputs={"mean": 1}, execution_name="my_execution", wait=True
    )

"""
