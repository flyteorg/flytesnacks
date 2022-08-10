KubeRay
===================

`KubeRay <https://github.com/ray-project/kuberay>`__ is an open source toolkit to run Ray applications on Kubernetes. It provides several tools to improve running and managing Ray on Kubernetes.
- Ray Operator
- Backend services to create/delete cluster resources
- Kubectl plugin/CLI to operate CRD objects
- Native Job and Serving integration with Clusters

Installation
------------

To install the Ray plugin, run the following command:

.. code-block:: bash

    pip install flytekitplugins-ray

To enable the plugin in the backend, follow instructions outlined in the :std:ref:`flyte:deployment-plugin-setup-k8s` guide.

Submit a Ray job to existing cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. testcode:: ray-quickstart-1
    import ray
    from flytekit import task
    from flytekitplugins.ray import RayJobConfig, WorkerNodeConfig, HeadNodeConfig

    @ray.remote
    def f(x):
        return x * x

    @task(task_config=RayJobConfig(
        address=<RAY_CLUSTER_ADDRESS>
        runtime_env={"pip": ["numpy", "pandas"]})
    )
    def ray_task() -> typing.List[int]:
        futures = [f.remote(i) for i in range(5)]
        return ray.get(futures)


Create a Ray cluster managed by Flyte and run a Ray job on this cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. testcode:: ray-quickstart-2
    @task(task_config=RayJobConfig(worker_node_config=[WorkerNodeConfig(group_name="test-group", replicas=10)])
    def ray_task() -> typing.List[int]:
        futures = [f.remote(i) for i in range(5)]
        return ray.get(futures)