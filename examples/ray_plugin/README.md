(kube-ray-op)=

# Ray

```{eval-rst}
.. tags:: Integration, DistributedComputing, KubernetesOperator, Advanced
```

[KubeRay](https://github.com/ray-project/kuberay) is an open-source toolkit designed to facilitate the execution of
Ray applications on Kubernetes. It offers a range of tools that enhance the operational aspects of
running and overseeing Ray on Kubernetes.

Key components include:

- Ray Operator
- Backend services for cluster resource creation and deletion
- Kubectl plugin/CLI for CRD object management
- Seamless integration of Jobs and Serving functionality with Clusters

## Install the plugin

To install the Ray plugin, run the following command:

```
pip install flytekitplugins-ray
```

To enable the plugin in the backend, follow instructions outlined in the {std:ref}`flyte:deployment-plugin-setup-k8s` guide.

## Implementation details

### Submit a Ray job to existing cluster

```{eval-rst}
.. testcode:: ray-quickstart-1
    import ray
    from flytekit import task
    from flytekitplugins.ray import RayJobConfig

    @ray.remote
    def f(x):
        return x * x

    @task(
        task_config=RayJobConfig(
            address=<RAY_CLUSTER_ADDRESS>
            runtime_env={"pip": ["numpy", "pandas"]}
        )
    )
    def ray_task() -> typing.List[int]:
        futures = [f.remote(i) for i in range(5)]
        return ray.get(futures)

```

### Create a Ray cluster managed by Flyte and run a Ray Job on the cluster

```{eval-rst}
.. testcode:: ray-quickstart-2
    import ray
    from flytekit import task
    from flytekitplugins.ray import RayJobConfig, WorkerNodeConfig, HeadNodeConfig

    @task(task_config=RayJobConfig(worker_node_config=[WorkerNodeConfig(group_name="test-group", replicas=10)]))
    def ray_task() -> typing.List[int]:
        futures = [f.remote(i) for i in range(5)]
        return ray.get(futures)
```

## Run the example on the Flyte cluster

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/ray_plugin/ray_plugin/ray_example.py \
  ray_workflow --n 10
```

```{auto-examples-toc}
ray_example
```
