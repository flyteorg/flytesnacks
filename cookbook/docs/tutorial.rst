.. _flyte-tutorial:
.. currentmodule:: flyte_tutorial

############################################
Hello, Flytekit!
############################################

.. rubric:: Estimated time to complete: 3 minutes.

``flytekit`` is simple to understand and inculcate it into your workflows. You're going to explore its simplicity through a ``Hello, Flytekit!`` example.

Prerequisites
*************

Ensure that you have `git <https://git-scm.com/>`__ installed in your workspace.

Steps
*****

1. First, install the Python Flytekit SDK and clone the ``flytesnacks`` repo.

.. prompt:: bash

  pip install --pre flytekit
  git clone git@github.com:flyteorg/flytesnacks.git flytesnacks
  cd flytesnacks

``flytesnacks`` constitutes the code example. 

2. The repo comes with some useful Make targets to make your experimentation workflow easier. Run ``make help`` to get the supported commands.
   
   For now, start a sandbox cluster.

.. prompt:: bash

   make start

This deploys a cluster in your workspace.
  
.. tip:: 
   Take a minute to explore the Flyte Console through the provided URL.

   .. image:: https://github.com/flyteorg/flyte/raw/static-resources/img/first-run-console-2.gif
       :alt: A quick visual tour for launching your first Workflow.

3. Open ``hello_flytekit.py`` in your favorite editor located at the following path:

.. code-block::

  cookbook/core/basic/hello_flytekit.py

5. Add ``name: str`` as an argument to both ``my_wf`` and ``say_hello`` functions. Then update the body of ``say_hello`` to consume that as an argument.

.. tip::

  .. code-block:: python

    @task
    def say_hello(name: str) -> str:
        return f"Hello, {name}!"

.. tip::

  .. code-block:: python

    @workflow
    def my_wf(name: str) -> str:
        res = say_hello(name=name)
        return res

The reason behind passing an argument is to help you get a hands-on experience as to how Flyte displays the inputs and outputs in its dashboard. 

6. Update the simple test (function call) present at the bottom of the file to pass in a name. 

.. tip::

  .. code-block:: python

    print(f"Running my_wf(name='Flyte Python SDK') {my_wf(name='Flyte Python SDK')}")

8. Now, run the below command in your terminal.

.. prompt:: bash

  python cookbook/core/basic/hello_flytekit.py

When you run this file locally, it should output ``Hello, Flyte Python SDK!``.

*Congratulations!* You successfully ran your first workflow! 

Now, run it on the sandbox cluster you deployed earlier.

6. Run the following command in the ``flytesnacks`` directory.

.. prompt:: bash

  REGISTRY=ghcr.io/flyteorg make fast_register

7. Visit `the console <http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/core.basic.hello_flytekit.my_wf>`__, click launch, and enter the input.

8. Give it a minute and once it's done, check out "Inputs/Outputs" on the top right corner to see your greeting updated.

.. image:: https://raw.githubusercontent.com/flyteorg/flyte/static-resources/img/flytesnacks/tutorial/exercise.gif
    :alt: A quick visual tour for launching a workflow and checking the outputs when it's done.

.. admonition:: Recap

  You have successfully:

  1. Ran a flyte sandbox cluster.
  2. Ran a flyte workflow locally.
  3. Ran a flyte workflow on a cluster.

Head over to the next section to :ref:`flyte-core` learn more about FlyteKit and how to start leveraging all the functionality flyte has to offer in simple and idiomatic python.
