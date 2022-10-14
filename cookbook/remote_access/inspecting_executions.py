"""
Inspecting Workflow and Task Executions
---------------------------------------

Using flyctl:
=============

Inspecting workflow and task executions are done in the same manner as below. For more details see the
`flytectl API reference <https://docs.flyte.org/projects/flytectl/en/stable/gen/flytectl_get_execution.html>`__.

Monitor the execution by providing the execution id from create command which can be task or workflow execution. ::

    flytectl get execution -p flytesnacks -d development <execid>

For more details use ``--details`` flag which shows node executions along with task executions on them. ::

    flytectl get execution -p flytesnacks -d development <execid> --details

If you prefer to see yaml/json view for the details then change the output format using the -o flag. ::

    flytectl get execution -p flytesnacks -d development <execid> --details -o yaml

To see the results of the execution you can inspect the node closure outputUri in detailed yaml output. ::

    "outputUri": "s3://my-s3-bucket/metadata/propeller/flytesnacks-development-<execid>/n0/data/0/outputs.pb"


Using flytekit (python):
========================
More details can be found in the docs for  `FlyteRemote <https://docs.flyte.org/projects/flytekit/en/latest/remote.html>`__

.. code-block:: python
    from flytekit.remote import FlyteRemote

    # FlyteRemote object is the main entrypoint to API
    remote = FlyteRemote(
        config=Config.for_endpoint(endpoint="flyte.example.net"),
        default_project="flytesnacks",
        default_domain="development",
    )
    
    execution = remote.fetch_execution(
        name="fb22e306a0d91e1c6000", project="flytesnacks", domain="development"
    )

    # Inspecting execution
    # The 'inputs' and 'outputs' correspond to the top-level execution or the workflow itself.
    input_keys = execution.inputs.keys()
    output_keys = execution.outputs.keys()

    # Fetching a specific output, say, a model file:
    model_file = execution.outputs["model_file"]
    with open(model_file) as f:
        # use mode
        ...

"""
