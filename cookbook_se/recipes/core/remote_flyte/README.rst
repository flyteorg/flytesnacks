Getting setup for remote execution
-------------------------------------
Flytekit provides a python SDK for authoring and executing workflows and tasks in python.
Flytekit comes with a simplistic local scheduler that executes code in a local environment.
But, to leverage the full power of Flyte, we recommend using a deployed backend of Flyte. Flyte can be run
on a kubernetes cluster - locally, in a cloud environment or on-prem.

Please refer to the `Installing Flyte <https://lyft.github.io/flyte/administrator/install/index.html>`_ for details on getting started with a Flyte installation.
This section walks through steps on deploying your local workflow to a distributed Flyte environment, with ``NO CODE CHANGES``.

Build your Dockerfile
^^^^^^^^^^^^^^^^^^^^^^
Now that you have workflows running locally, its time to take them for a spin onto a Hosted Flyte backend.

.. literalinclude:: ../../Dockerfile
    :language: dockerfile
    :emphasize-lines: 1
    :linenos:


Serialize your workflows and tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Register your Workflows and Tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _working_hosted_service:

Some concepts available remote only
-----------------------------------
