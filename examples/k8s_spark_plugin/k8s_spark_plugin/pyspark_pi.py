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
from flytekit import ImageSpec, Resources, task, workflow

# %% [markdown]
# Create an `ImageSpec` to automate the retrieval of a prebuilt Spark image.
# %%
custom_image = ImageSpec(registry="localhost:30000")

# %% [markdown]
# :::{note}
# To upload the image to the local registry in the demo cluster, indicate the registry as `localhost:30000`.
# :::
#
# The following imports are required to configure the Spark cluster in Flyte.
# You can load them on demand.
# %%
if custom_image.is_container():
    from flytekitplugins.spark import Spark


# %% [markdown]
# To create a Spark task, add {py:class}`~flytekitplugins.spark.Spark` config to the Flyte task.
#
# The `spark_conf` parameter can encompass configuration choices commonly employed when setting up a Spark cluster.
# Additionally, if necessary, you can provide `hadoop_conf` as an input.
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
        }
    ),
    limits=Resources(mem="2000M"),
    container_image=custom_image,
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
@task(cache_version="2")
def print_every_time(value_to_print: float, date_triggered: datetime.datetime) -> int:
    print("My printed value: {} @ {}".format(value_to_print, date_triggered))
    return 1


# %% [markdown]
# Finally, define a workflow that connects your tasks in a sequence.
# Remember, Spark and non-Spark tasks can be chained together as long as their parameter specifications match.
# %%
@workflow
def my_spark(triggered_date: datetime.datetime = datetime.datetime.now()) -> float:
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
