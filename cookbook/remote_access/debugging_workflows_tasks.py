"""
Debugging Workflow and Task Executions
--------------------------------------

The inspection of task and workflow execution would provide you log links to debug things further

Using ``--details`` flag would shows you node executions view with log links. ::


        └── n1 - FAILED - 2021-06-30 08:51:07.3111846 +0000 UTC - 2021-06-30 08:51:17.192852 +0000 UTC
        │   ├── Attempt :0
        │       └── Task - FAILED - 2021-06-30 08:51:07.3111846 +0000 UTC - 2021-06-30 08:51:17.192852 +0000 UTC
        │       └── Logs :
        │           └── Name :Kubernetes Logs (User)
        │           └── URI :http://localhost:30082/#/log/flytectldemo-development/f3a5a4034960f4aa1a09-n1-0/pod?namespace=flytectldemo-development

Additionally you can check the pods launched by flyte in <project>-<domain> namespace ::

    kubectl get pods -n <project>-<domain>

The launched pods will have a prefix of execution name along with suffix of nodeId ::

        NAME                        READY   STATUS             RESTARTS   AGE
        f65009af77f284e50959-n0-0   0/1     ErrImagePull       0          18h

So here the investigation can move ahead by describing the pod and checking the issue with Image pull.

Using flytekit (python):
========================
For how to inspect an execution, go back to `Inspecting Workflow and Task Executions <https://docs.flyte.org/projects/cookbook/en/latest/auto/remote_access/inspecting_executions.html>`__

More details can be found in the docs for  `FlyteRemote <https://docs.flyte.org/projects/flytekit/en/latest/remote.html>`__

.. code-block:: python
        from flytekit.remote import FlyteRemote

        # FlyteRemote object is the main entrypoint to API
        remote = FlyteRemote(
                config=Config.for_endpoint(endpoint="flyte.example.net"),
                default_project="flytesnacks",
                default_domain="development",
        )
        
        # Fetch execution
        execution = remote.fetch_execution(
                name="fb22e306a0d91e1c6000", project="flytesnacks", domain="development"
        )

        # You can use FlyteRemote.sync() to to sync the entity object's state with the remote state during the execution run
        synced_execution = remote.sync(execution, sync_nodes=True)
        node_keys = synced_execution.node_executions.keys()

During the sync, you may come across ``Received message larger than max (xxx vs. 4194304)`` error if the message size is too large. 

In that case, edit the ``flyte-admin-base-config`` config map using the command ``kubectl edit cm flyte-admin-base-config -n flyte`` 
to increase the ``maxMessageSizeBytes`` value. 

Refer to the `troubleshooting guide <https://docs.flyte.org/en/latest/community/troubleshoot.html>` for more info.

``node_executions`` will fetch all the underlying node executions recursively.

To fetch output of a specific node execution:
.. code-block:: python
        node_execution_output = synced_execution.node_executions["n1"].outputs["model_file"]

"""
