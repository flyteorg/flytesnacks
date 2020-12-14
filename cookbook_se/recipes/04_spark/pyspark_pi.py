"""
Passing Spark DataSets from user functions
------------------------------------------

This example shows how flytekit simplifies usage of pyspark in a users code.
The task ``hello_spark`` runs a new spark cluster, which when run locally runs a single node client only cluster,
but when run remote spins up a arbitrarily sized cluster depending on the specified spark configuration. ``spark_conf``

This Example also shows how a user can simply create 2 tasks, that use different Docker images. This makes it possible
to completely separate the image creation between for different tasks, thus reducing the size of images. For example
a spark image needs JVM, spark jars and other bits installed, while a python task only needs python and libraries for
python installed.

Moreover, this also makes it possible to separate images for Deep learning that contain nvidia drivers.

To support multiple images, flytekit allows the container images to be parameterized as follows

 ``{{.image.<name>.<attribute>}}``
   the name of the image in the image configuration. The name ``default`` is a reserved keyword and will automatically
   apply to the default image name for this repository
   attribute can be either ``fqn`` or ``version``
   ``fqn`` refers to the fully qualified name of the image. For example it includes the repository and domain url of the
          image. e.g. docker.io/my_repo/xyz
   ``version`` refers to the tag of the image. e.g. latest, or python-3.8 etc.

If the container_image is not specified then the default configured image for the project is used.

"""
import flytekit
import random
import datetime
from operator import add
from flytekit import task, workflow
from flytekit.taskplugins.spark import Spark


@task(task_config=Spark(
    # this configuration is applied to the spark cluster
    spark_conf={
        'spark.driver.memory': "1000M",
        'spark.executor.memory': "1000M",
        'spark.executor.cores': '1',
        'spark.executor.instances': '2',
        'spark.driver.cores': '1',
    }),
    cache_version='1',
    # a separate image is used
    container_image='{{.image.default.fqn}}:spark-{{.image.default.version}}')
def hello_spark(partitions: int) -> float:
    print("Starting Spark with Partitions: {}".format(partitions))

    n = 100000 * partitions
    sess = flytekit.current_context().spark_session
    count = sess.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    pi_val = 4.0 * count / n
    print("Pi val is :{}".format(pi_val))
    return pi_val


@task(cache_version='1')
def print_every_time(value_to_print: float, date_triggered: datetime.datetime) -> int:
    print("My printed value: {} @ {}".format(value_to_print, date_triggered))
    return 1


def f(_):
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    return 1 if x ** 2 + y ** 2 <= 1 else 0


@workflow
def my_spark(triggered_date: datetime.datetime) -> float:
    """
    Using the workflow is still as any other workflow. As image is a property of the task, the workflow does not care
    about how the image is configured.
    """
    pi = hello_spark(partitions=50)
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi


if __name__ == "__main__":
    """
    NOTE: To run a multi-image workflow locally, all dependencies of all the tasks should be installed, ignoring which
    may result in local runtime failures.
    """
    print(f"Running {__file__} main...")
    print(f"Running my_spark(triggered_date=datetime.datetime.now()){my_spark(triggered_date=datetime.datetime.now())}")
