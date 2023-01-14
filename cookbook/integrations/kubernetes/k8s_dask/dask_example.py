"""
.. _intermediate_using_dask_tasks:

Writing a Dask Task
----------------------

Flyte has an optional plugin that makes it possible to run `Dask <https://www.dask.org/>`__ jobs natively on your
kubernetes cluster. It makes it extremely easy to run your ``dask`` code as a task. The plugin creates a new
virtual/ephemeral cluster for each ``dask`` task, where Flyte manages the cluster lifecycle.

Dask in flytekit
================
For a more complete example refer to the :std:ref:`example-dask`

#. Enable the ``dask`` plugin in the backend, following the steps from the previous section
#. Install the `flytekit dask plugin <https://pypi.org/project/flytekitplugins-dask/>`__ ::

    pip install flytekitplugins-dask

#. Write regular ``dask`` code - with one change in the ``@task`` decorator. Refer to the example below:

    .. code-block:: python

        @task(
            task_config=Dask(
                job_pod_spec=JobPodSpec(
                    limits=Resources(cpu="1", mem="2Gi"),
                ),
                cluster=DaskCluster(
                    n_workers=10,
                    limits=Resources(cpu="4", mem="10Gi"),
                ),
            ),
            cache_version="1",
            cache=True,
        )
        def hello_dask(size: int) -> float:
            ...
            client = Client()  # Create a client as you would in local code
            # Regular dask code
            ...


#. Run it locally

   .. code-block:: python

       hello_dask(size=10)

#. Use it in a workflow
#. Run it on a remote cluster


Examples
========

.. _example-dask:

How Flytekit Simplifies the Usage of dask in User Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The task ``hello_dask`` runs a new dask cluster, which when run locally starts a local ``dask`` cluster, but when run
remote spins up an arbitrarily sized cluster depending on the specified dask configuration.

"""

from dask import array as da
from flytekit import Resources, task

# %%
# The following imports are required to configure the Dask cluster in Flyte
from flytekitplugins.dask import Dask, WorkerGroup

# %%
# Dask Task Sample
# ^^^^^^^^^^^^^^^^
#
# This example shows how a Dask task can be written simply by adding a ``@task(task_config=Dask(...), ...)`` decorator.
# Refer to the `Dask <https://github.com/flyteorg/flytekit/blob/4b1675ffb85648dc5742e9a6dea98b94714963e1/plugins/flytekit-dask/flytekitplugins/dask/task.py#L54-L63>`__
# class to understand the various configuration options.


@task(
    task_config=Dask(
        workers=WorkerGroup(
            number_of_workers=10,
            limits=Resources(cpu="4", mem="10Gi"),
        ),
    ),
    limits=Resources(cpu="1", mem="2Gi"),
    cache_version="1",
    cache=True,
)
def hello_dask(size: int) -> float:
    # Dask will implicitly create a Client in the background by calling Client(). When executing
    # remotely, this Client() will use the deployed ``dask`` cluster.
    array = da.random.random(size)
    return float(array.mean().compute())


# %%
# The function can be executed locally:
# Guard with:
#
#   if __name__ == '__main__':
#
# in a local Python script
print(hello_dask(size=1000))
