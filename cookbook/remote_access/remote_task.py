"""
Running a Task
--------------------

Using flyctl:
=============

This is multi-steps process as well where we create an execution spec file, update the spec file and then create the execution.
More details can be found `here <https://docs.flyte.org/projects/flytectl/en/stable/gen/flytectl_create_execution.html>`__

**Generate execution spec file** ::

    flytectl get tasks -d development -p flytectldemo core.advanced.merge_sort.merge  --latest --execFile exec_spec.yaml

**Update the input spec file for arguments to the workflow** ::

            iamRoleARN: 'arn:aws:iam::12345678:role/defaultrole'
            inputs:
              sorted_list1:
              - 2
              - 4
              - 6
              sorted_list2:
              - 1
              - 3
              - 5
            kubeServiceAcct: ""
            targetDomain: ""
            targetProject: ""
            task: core.advanced.merge_sort.merge
            version: "v1"

**Create execution using the exec spec file** ::

    flytectl create execution -p flytesnacks -d development --execFile exec_spec.yaml


**Monitor the execution by providing the execution id from create command** ::

    flytectl get execution -p flytesnacks -d development <execid>


Using flytekit (python):
========================
More details can be found in the docs for  `FlyteRemote <https://docs.flyte.org/projects/flytekit/en/latest/remote.html>`__

.. code-block:: python
    from flytekit.remote import FlyteRemote
    from flytekit.configuration import Config, SerializationSettings

    # FlyteRemote object is the main entrypoint to API
    remote = FlyteRemote(
        config=Config.for_endpoint(endpoint="flyte.example.net"),
        default_project="flytesnacks",
        default_domain="development",
    )

    # Get Task
    task_1 = remote.fetch_task(name="core.basic.hello_world.say_hello", version="v1")

    # Tasks, workflows, and launch plans can be registered using FlyteRemote.
    flyte_entity = ...
    flyte_task = remote.register_task(
        entity=flyte_entity,
        serialization_settings=SerializationSettings(image_config=None),
        version="v1",
    )
    flyte_workflow = remote.register_workflow(
        entity=flyte_entity,
        serialization_settings=SerializationSettings(image_config=None),
        version="v1",
    )
    flyte_launch_plan = remote.register_launch_plan(entity=flyte_entity, version="v1")

    # Run Task
    execution = remote.execute(
        task_1, inputs={...}, execution_name="my_execution", wait=True
    )

    # Inspecting execution
    # The 'inputs' and 'outputs' correspond to the top-level execution or the workflow itself.
    input_keys = execution.inputs.keys()
    output_keys = execution.outputs.keys()

"""
