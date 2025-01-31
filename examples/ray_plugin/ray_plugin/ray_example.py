# %% [markdown]
# # Running Ray Tasks
#
# The Ray task offers the capability to execute a Ray job either on a pre-existing Ray cluster
# or by creating a new Ray cluster using the Ray operator.
#
# :::{Warning}
# **Version Compatibility**
# - flyte >= 1.11.1-b1 only works with kuberay 1.1.0
# - Although flyte < 1.11.0 can work with kuberay 0.6.0 and 1.1.0, we strongly recommend upgrading to the latest flyte and kuberay 1.1.0 for stability and usability
# :::
#
# To begin, load the libraries.
# %%
import typing

from flytekit import ImageSpec, Resources, task, workflow

# %% [markdown]
# Create an `ImageSpec` to encompass all the dependencies needed for the Ray task.
# :::{important}
# Replace `ghcr.io/flyteorg` with a container registry you've access to publish to.
# To upload the image to the local registry in the demo cluster, indicate the registry as `localhost:30000`.
# :::
# %%
custom_image = ImageSpec(
    registry="ghcr.io/flyteorg",
    packages=["flytekitplugins-ray"],
    # kuberay operator needs wget for readiness probe.
    apt_packages=["wget"],
)

import ray
from flytekitplugins.ray import HeadNodeConfig, RayJobConfig, WorkerNodeConfig


# %% [markdown]
# In this example, we define a [remote function](https://docs.ray.io/en/latest/ray-core/tasks.html#tasks)
# that will be executed asynchronously in the Ray cluster.
# %%
@ray.remote
def f(x):
    return x * x


# %% [markdown]
# Include both {py:class}`~flytekitplugins.ray.HeadNodeConfig` and
# {py:class}`~flytekitplugins.ray.WorkerNodeConfig` in {py:class}`~flytekitplugins.ray.RayJobConfig`.
# These configurations will subsequently be employed by the Ray operator to establish a Ray cluster before task execution.
#
# Here's a breakdown of the parameters:
#
# - `ray_start_params`: These are the [parameters](https://docs.ray.io/en/latest/ray-core/api/doc/ray.init.html)
#   used in the Ray `init` method, encompassing the address and object-store-memory settings.
# - `replicas`: Specifies the desired number of replicas for the worker group. The default is 1.
# - `group_name`: A RayCluster can host multiple worker groups, each differentiated by its name.
# - `runtime_env`: The [runtime environment](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html#runtime-environments)
# - `enable_autoscaling`: Enable [Ray Autoscaler](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/configuring-autoscaling.html)
# - `ttl_seconds_after_finished`: Shutdown Ray cluster after 1 hour of inactivity.
#   definition outlines the necessary dependencies for your Ray application to function.
#   This environment is dynamically installed on the cluster at runtime.
# %%
ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "True"}),
    worker_node_config=[WorkerNodeConfig(group_name="ray-group", replicas=1)],
    runtime_env={"pip": ["numpy", "pandas"]},  # or runtime_env="./requirements.txt"
    enable_autoscaling=True,
    shutdown_after_job_finishes=True,
    ttl_seconds_after_finished=3600,
)


# %% [markdown]
# Create a Ray task. The task is invoked on the Ray head node, while `f.remote(i)` executes asynchronously on distinct Ray workers.
# %%
@task(
    task_config=ray_config,
    requests=Resources(mem="2Gi", cpu="2"),
    container_image=custom_image,
)
def ray_task(n: int) -> typing.List[int]:
    futures = [f.remote(i) for i in range(n)]
    return ray.get(futures)


# %% [markdown]
# :::{note}
# The `Resources` section here is utilized to specify the resources allocated to all Ray components like head, worker & driver pods.
# %% [markdown]
# For more fine grain resource allocation, you are able to set the resources for Ray head & worker pods by setting `requests` and/or `limits` for the respective config.
# %%
ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "True"}, requests=Resources(cpu="1", mem="2Gi")),
    worker_node_config=[
        WorkerNodeConfig(
            group_name="ray-group",
            replicas=1,
            requests=Resources(cpu="2", mem="2Gi"),
            limits=Resources(cpu="3", mem="6Gi"),
        )
    ],
    runtime_env={"pip": ["numpy", "pandas"]},  # or runtime_env="./requirements.txt"
    enable_autoscaling=True,
    shutdown_after_job_finishes=True,
    ttl_seconds_after_finished=3600,
)


# Lastly, define a workflow to call the Ray task.
# %%
@workflow
def ray_workflow(n: int) -> typing.List[int]:
    return ray_task(n=n)


# %% [markdown]
# You have the option to execute the code locally,
# during which Flyte generates a self-contained Ray cluster on your local environment.
# %%
if __name__ == "__main__":
    print(ray_workflow(n=10))

# %% [markdown]
# ## Troubleshoot
#
# If you observe that the head and worker pods are not being generated, you need to ensure that `ray[default]` is installed since it supports
# the cluster and dashboard launcher.
#
# Another potential error might involve ingress issues, as indicated in the kuberay-operator logs.
# If you encounter an error resembling the following:
#
# ````
# ERROR controllers.RayCluster Ingress create error!
# {
#     "Ingress.Error": "Internal error occurred: failed calling webhook "validate.nginx.ingress.kubernetes.io": failed to call webhook: Post "<https://nginx-ingress-ingress-nginx-controller-admission.default.svc:443/networking/v1/ingresses?timeout=10s>": no endpoints available for service "nginx-ingress-ingress-nginx-controller-admission"",
#     "error": "Internal error occurred: failed calling webhook "validate.nginx.ingress.kubernetes.io": failed to call webhook: Post "<https://nginx-ingress-ingress-nginx-controller-admission.default.svc:443/networking/v1/ingresses?timeout=10s>": no endpoints available for service "nginx-ingress-ingress-nginx-controller-admission""
# }
# ````
#
# You must ensure that the ingress controller is [installed](https://docs.flyte.org/en/latest/deployment/gcp/manual.html#ingress).
