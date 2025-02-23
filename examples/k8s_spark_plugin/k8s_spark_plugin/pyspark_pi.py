# %% [markdown]
# (spark_task)=
#
# # Running a Spark Task
#
# To begin, import the necessary dependencies.
# %%
import datetime
import random
from operator import add

import flytekit
from flytekit import ImageSpec, PodTemplate, Resources, task, workflow
from flytekitplugins.spark import Spark
from kubernetes.client.models import (
    V1Container,
    V1EnvVar,
    V1PodSpec,
    V1Toleration,
)

# %% [markdown]
# Create an `ImageSpec` to automate the retrieval of a prebuilt Spark image.
# %%
custom_image = ImageSpec(python_version="3.9", registry="ghcr.io/flyteorg", packages=["flytekitplugins-spark"])


# %% [markdown]
# :::{important}
# Replace `ghcr.io/flyteorg` with a container registry you've access to publish to.
# To upload the image to the local registry in the demo cluster, indicate the registry as `localhost:30000`.
# :::
#
# Optionally, define pod templates for driver and executor.
# %%
driver_pod = PodTemplate(
    labels={"lKeyA_d": "lValA", "lKeyB_d": "lValB"},
    annotations={"aKeyA_d": "aValA", "aKeyB_d": "aValB"},
    primary_container_name="driver-primary",
    pod_spec=V1PodSpec(
        containers=[
            V1Container(
                name="driver-primary",
                image="ghcr.io/flyteorg",
                command=["echo"],
                args=["wow"],
                env=[V1EnvVar(name="x/custom-driver", value="driver")],
            ),
            V1Container(
                name="not-primary",
                command=["echo"],
                args=["not_primary"],
            ),
        ],
        tolerations=[
            V1Toleration(
                key="x/custom-driver",
                operator="Equal",
                value="foo-driver",
                effect="NoSchedule",
            ),
        ],
    ),
)

executor_pod = PodTemplate(
    labels={"lKeyA_e": "lValA", "lKeyB_e": "lValB"},
    annotations={"aKeyA_e": "aValA", "aKeyB_e": "aValB"},
    primary_container_name="executor-primary",
    pod_spec=V1PodSpec(
        containers=[
            V1Container(
                name="executor-primary",
                image="ghcr.io/flyteorg",
                command=["echo"],
                args=["wow"],
                env=[V1EnvVar(name="x/custom-executor", value="executor")],
            ),
            V1Container(
                name="not-primary",
                command=["echo"],
                args=["not_primary"],
            ),
        ],
        tolerations=[
            V1Toleration(
                key="x/custom-executor",
                operator="Equal",
                value="foo-executor",
                effect="NoSchedule",
            ),
        ],
    ),
)


# %% [markdown]
# To create a Spark task, add {py:class}`~flytekitplugins.spark.Spark` config to the Flyte task.
#
# The `spark_conf` parameter can encompass configuration choices commonly employed when setting up a Spark cluster.
# Additionally, if necessary, you can provide `hadoop_conf` as an input.
#
# Users can set `driver_pod` and `executor_pod` to customize pod template for driver and executor.
# If these are not set, the `pod_template` specified in `@task` will be used as the default.
# %%
@task(
    task_config=Spark(
        # This configuration is applied to the Spark cluster
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
            "spark.jars": "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar",
        },
        driver_pod=driver_pod,
        executor_pod=executor_pod,
    ),
    limits=Resources(mem="2000M"),
    container_image=custom_image,
    pod_template=PodTemplate(
        labels={"lKeyA": "lValA", "lKeyB": "lValB"},
        annotations={"aKeyA": "aValA", "aKeyB": "aValB"},
        pod_spec=V1PodSpec(
            containers=[
                V1Container(
                    name="primary",
                    image=custom_image,
                    command="echo",
                    args=["wow"],
                    env=[V1EnvVar(name="x/custom", value="custom")],
                ),
            ],
            tolerations=[
                V1Toleration(
                    key="x/custom",
                    operator="Equal",
                    value="foo",
                    effect="NoSchedule",
                ),
            ],
        ),
    ),
)
def hello_spark(partitions: int) -> float:
    print("Starting Spark with Partitions: {}".format(partitions))

    n = 1 * partitions
    sess = flytekit.current_context().spark_session
    count = sess.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)

    pi_val = 4.0 * count / n
    return pi_val


# %% [markdown]
# The `hello_spark` task initiates a new Spark cluster.
# When executed locally, it sets up a single-node client-only cluster.
# However, when executed remotely, it dynamically scales the cluster size based on the specified Spark configuration.
#
# For this particular example,
# we define a function upon which the map-reduce operation is invoked within the Spark cluster.
# %%
def f(_):
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    return 1 if x**2 + y**2 <= 1 else 0


# %% [markdown]
# Additionally, we specify a standard Flyte task that won't be executed on the Spark cluster.
# %%
@task(
    cache_version="2",
    container_image=custom_image,
)
def print_every_time(value_to_print: float, date_triggered: datetime.datetime) -> int:
    print("My printed value: {} @ {}".format(value_to_print, date_triggered))
    return 1


# %% [markdown]
# Finally, define a workflow that connects your tasks in a sequence.
# Remember, Spark and non-Spark tasks can be chained together as long as their parameter specifications match.
# %%
@workflow
def my_spark(triggered_date: datetime.datetime = datetime.datetime(2020, 9, 11)) -> float:
    """
    Using the workflow is still as any other workflow. As image is a property of the task, the workflow does not care
    about how the image is configured.
    """
    pi = hello_spark(partitions=1)
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi


# %% [markdown]
# You can execute the workflow locally.
# Certain aspects of Spark, such as links to {ref}`Hive <Hive>` meta stores, may not work in the local execution,
# but these limitations are inherent to using Spark and are not introduced by Flyte.
# %%
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running my_spark(triggered_date=datetime.datetime.now()) {my_spark(triggered_date=datetime.datetime.now())}"
    )
