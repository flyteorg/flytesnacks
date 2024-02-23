# %% [markdown]
# (mmcloud_example)=
# # Memory Machine Cloud
#
# This example shows how to use the MMCloud plugin to execute tasks on MemVerge Memory Machine Cloud.

# %%
from flytekit import Resources, task, workflow
from flytekitplugins.mmcloud import MMCloudConfig

# %% [markdown]
# `MMCloudConfig` configures `MMCloudTask`. Tasks specified with `MMCloudConfig` will be executed using MMCloud. Tasks will be executed with requests `cpu="1"` and `mem="1Gi"` by default.

# %%
@task(task_config=MMCloudConfig())
def to_str(i: int) -> str:
    return str(i)


@task(task_config=MMCloudConfig())
def to_int(s: str) -> int:
    return int(s)


# %% [markdown]
# [Resource](https://docs.flyte.org/projects/cookbook/en/latest/auto_examples/productionizing/customizing_resources.html) (cpu and mem) requests and limits, [container](https://docs.flyte.org/projects/cookbook/en/latest/auto_examples/customizing_dependencies/multi_images.html) images, and [environment](https://docs.flyte.org/projects/flytekit/en/latest/generated/flytekit.task.html) variable specifications are supported.

# %%
@task(
    task_config=MMCloudConfig(submit_extra="--migratePolicy [enable=true]"),
    requests=Resources(cpu="1", mem="1Gi"),
    limits=Resources(cpu="2", mem="4Gi"),
    environment={"KEY": "value"},
)
def concatenate_str(s1: str, s2: str) -> str:
    return s1 + s2


@workflow
def concatenate_int_wf(i1: int, i2: int) -> int:
    i1_str = to_str(i=i1)
    i2_str = to_str(i=i2)
    return to_int(s=concatenate_str(s1=i1_str, s2=i2_str))
