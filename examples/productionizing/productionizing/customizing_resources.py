# %% [markdown]
# # Customizing Task Resources
#
# ```{eval-rst}
# .. tags:: Deployment, Infrastructure, Basic
# ```
#
# One of the reasons to use a hosted Flyte environment is the potential of leveraging CPU, memory and storage resources, far greater than what's available locally.
# Flytekit makes it possible to specify these requirements declaratively and close to where the task itself is declared.

# %% [markdown]
# In this example, the memory required by the function increases as the dataset size increases.
# Large datasets may not be able to run locally, so we would want to provide hints to the Flyte backend to request for more memory.
# This is done by decorating the task with the hints as shown in the following code sample.
#
# Tasks can have `task_config` which provides configuration for a specific task types, or `requests` and `limits` which mirror the native [equivalents in Kubernetes](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits).
# A task can possibly be allocated more resources than it requests, but never more than its limit.
# Requests are treated as hints to schedule tasks on nodes with available resources, whereas limits
# are hard constraints.
#
# For either a request or limit, refer to the {py:class}`flytekit:flytekit.Resources` documentation.
#
# And for task_config,  refer to the {py:func}`flytekit:flytekit.task` documentation.
#
# The following attributes can be specified for a `Resource`.
#
# 1. `cpu`
# 2. `mem`
# 3. `gpu`
#
# To ensure that regular tasks that don't require GPUs are not scheduled on GPU nodes, a separate node group for GPU nodes can be configured with [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).
#
# To ensure that tasks that require GPUs get the needed tolerations on their pods, set up FlytePropeller using the following [configuration](https://github.com/flyteorg/flytepropeller/blob/v0.10.5/config.yaml#L51,L56). Ensure that this toleration config matches the taint config you have configured to protect your GPU providing nodes from dealing with regular non-GPU workloads (pods).
#
# The actual values follow the [Kubernetes convention](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes).
# Let's look at an example to understand how to customize resources.

# %% [markdown]
# Import the dependencies.
# %%
import typing

from flytekit import Resources, task, workflow


# %% [markdown]
# Define a task and configure the resources to be allocated to it.
# %%
@task(requests=Resources(cpu="1", mem="100Mi"), limits=Resources(cpu="2", mem="150Mi"))
def count_unique_numbers(x: typing.List[int]) -> int:
    s = set()
    for i in x:
        s.add(i)
    return len(s)


# %% [markdown]
# Define a task that computes the square of a number.
# %%
@task
def square(x: int) -> int:
    return x * x


# %% [markdown]
# You can use the tasks decorated with memory and storage hints like regular tasks in a workflow.
# %%
@workflow
def my_workflow(x: typing.List[int]) -> int:
    return square(x=count_unique_numbers(x=x))


# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(count_unique_numbers(x=[1, 1, 2]))
    print(my_workflow(x=[1, 1, 2]))

# %% [markdown]
# :::{note}
# To alter the limits of the default platform configuration, change the [admin config](https://github.com/flyteorg/flyte/blob/b16ffd76934d690068db1265ac9907a278fba2ee/deployment/eks/flyte_helm_generated.yaml#L203-L213) and [namespace level quota](https://github.com/flyteorg/flyte/blob/b16ffd76934d690068db1265ac9907a278fba2ee/deployment/eks/flyte_helm_generated.yaml#L214-L240) on the cluster.
# :::

# %% [markdown]
# (resource_with_overrides)=
#
# ## Using `with_overrides`
#
# You can use the `with_overrides` method to override the resources allocated to the tasks dynamically.
# Let's understand how the resources can be initialized with an example.

# %% [markdown]
# Import the dependencies.
# %%
import typing  # noqa: E402

from flytekit import Resources, task, workflow, dynamic  # noqa: E402
from flytekitplugins.kftensorflow import PS, Chief, TfJob, Worker   # noqa: E402


# %% [markdown]
# Define a task and configure the resources to be allocated to it.
# You can use tasks decorated with memory and storage hints like regular tasks in a workflow, or configuration for an {py:class}`flytekitplugins:flytekitplugins.kftensorflow.TfJob` that can run distributed TensorFlow training on Kubernetes.
# %%
@task(
    task_config=TfJob(
        num_workers=1,
        num_ps_replicas=1,
        num_chief_replicas=1,
    ),
    requests=Resources(cpu="1", mem="200Mi"),
    limits=Resources(cpu="2", mem="350Mi"),
)
def run_tfjob() -> str:

    return "hello world"

# %% [markdown]
# The `with_overrides` method overrides the old resource allocations.
# %%
@workflow
def my_run() -> str:
    return run_tfjob().with_overrides(limits=Resources(cpu="6", mem="500Mi"))


# %% [markdown]
# Or you can use `@dynamic` to generate tasks at runtime with any custom configurations you may want.
# %%
@dynamic
def dynamic_run(num_workers: int) -> str:
    return run_tfjob().with_overrides(task_config=TfJob(
        num_workers=num_workers,
        num_ps_replicas=1,
        num_chief_replicas=1))
@workflow
def start_dynamic_run(new_num_workers: int) -> str:
    return dynamic_run(num_workers=new_num_workers)

# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(f"Running my_run(): {my_run()}")
    print(f"Running dynamic_run(num_workers=4): {start_dynamic_run(new_num_workers=4)}")

# %% [markdown]
# You can see the memory allocation below. The memory limit is `500Mi` rather than `350Mi`, and the
# CPU limit is 4, whereas it should have been 6 as specified using `with_overrides`.
# This is because the default platform CPU quota for every pod is 4.
#
# :::{figure} https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/core/resource_allocation.png
# :alt: Resource allocated using "with_overrides" method
#
# Resource allocated using "with_overrides" method
# :::
#
