"""
Running a Launchplan
--------------------

Using flyctl:
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

Using flytekit (python):
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
        name="my_workflow", version="v1", project="flytesnacks", domain="development"
    )

    # Get or create attached launchplan
    launch_plan = LaunchPlan.get_or_create(name="my_launch_plan", workflow=flyte_workflow)

    # You can register launch plans
    flyte_launch_plan = remote.register_launch_plan(entity=launch_plan, version="v1")

    # Execute launch plan
    execution = remote.execute(
        flyte_launch_plan, inputs={...}, execution_name="my_execution", wait=True
    )

    # Inspecting execution
    # The 'inputs' and 'outputs' correspond to the top-level execution or the workflow itself.
    input_keys = execution.inputs.keys()
    output_keys = execution.outputs.keys()

"""
