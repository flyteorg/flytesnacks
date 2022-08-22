import typing

import ray
from flytekit import Resources, task, workflow
from flytekitplugins.ray import HeadNodeConfig, RayJobConfig, WorkerNodeConfig


@ray.remote
def f(x):
    return x * x


ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "True"}),
    worker_node_config=[WorkerNodeConfig(group_name="ray-group", replicas=2)],
    runtime_env={"pip": "./requirements.txt"},
)

@task(task_config=ray_config, limits=Resources(mem="2000Mi", cpu="1"))
def ray_task(n: int) -> typing.List[int]:
    futures = [f.remote(i) for i in range(n)]
    return ray.get(futures)

@task
def task(n: typing.List[int]) -> typing.List[int]:
    return [i*i for i in range(n)]

@workflow
def ray_workflow(n: int) -> typing.List[int]:
    return ray_task(n=n)


# %%
# We can run the code locally wherein Flyte creates a standalone Ray cluster locally.
if __name__ == "__main__":
    print(ray_workflow(n=10))
