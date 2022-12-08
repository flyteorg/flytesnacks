"""
.. _spark_tasks_on_databricks:

Running a PySpark Task on Databricks Platform
---------------------------------------------
Flyte has an optional plugin that makes it possible to run `Apache Spark <https://spark.apache.org/>`_ jobs natively on your databricks spark cluster.
It makes it extremely easy to run your pyspark code as a task. The plugin creates a new ephemeral cluster for the spark execution dynamically.


Spark on databricks
===================
For a more complete example refer to the :std:ref:`example-spark`

#. Ensure you have ``flytekit>=0.16.0``
#. Enable Spark in backend, following the previous section.
#. Install the `flytekit spark plugin <https://pypi.org/project/flytekitplugins-spark/>`_ ::

    pip install flytekitplugins-spark

#. Upload an entrypoint.py to dbfs or s3. Spark driver node run this file to override the default command in the dbx job.

   .. code-block:: python

       # entrypoint.py
       import os
       import subprocess
       import sys

       def main():
           args = sys.argv
           p = subprocess.run(args[1:], capture_output=True)
           print("==========================stdout==============================")
           print(p.stdout.decode('utf-8'))
           print("==========================stderr==============================")
           print(p.stderr.decode('utf-8'))
           if p.stderr:
               exit(1)

       if __name__ == '__main__':
           main()

#. Generate a Databricks `access token <https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens>`_ for propeller, so it will be able to submit the job request to Databricks platform.
 After that, create a secret containing the token like below, and it should be mounted into the propeller.

   .. code-block:: yaml

      apiVersion: v1
      kind: Secret
      metadata:
        name: databricks-token
        namespace: flyte
      type: Opaque
      data:
        FLYTE_DATABRICKS_API_TOKEN: <API_TOKEN>

#. Create a `Instance Profile <https://docs.databricks.com/administration-guide/cloud-configurations/aws/instance-profiles.html>`_ for the Spark cluster, it allows the spark job to access your data in the s3 bucket.

#. Write regular pyspark code - with one change in ``@task`` decorator. Refer to the example below:

   .. code-block:: python

       @task(
           task_config=Spark(
               # this configuration is applied to the spark cluster
               spark_conf={
                   "spark.executor.instances": "2",
               }
               databricks_conf={
                   # The config is equal to the databricks job request.
                   # https://docs.databricks.com/dev-tools/api/2.0/jobs.html#request-structure
                   "run_name": "flytekit databricks plugin example",
                   "new_cluster": {
                       "spark_version": "11.0.x-scala2.12",
                       "node_type_id": "r3.xlarge",
                       "aws_attributes": {
                           "availability": "ON_DEMAND",
                           "instance_profile_arn": "arn:aws:iam::590375263360:instance-profile/databricks-s3-role",
                       },
                       "num_workers": 4,
                   },
                   "timeout_seconds": 3600,
                   "max_retries": 1,
               }
           ),
       )
       def hello_spark(partitions: int) -> float:
           ...
           sess = flytekit.current_context().spark_session
           # Regular Pypsark code
           ...


#. Run it locally

   .. code-block:: python

       hello_spark(partitions=10)

#. Use it in a workflow (check cookbook)
#. Run it on a remote cluster - To do this, you can have to build a custom image. Follow this `guide <https://docs.databricks.com/clusters/custom-containers.html>`_ to build a custom image. However, you can use default image provided by databricks, but make sure to add flytekit to the pypi config in the databricks config. Note: using default image only works in the fast-register mode because the workflow code isn't located in the image.

Examples
========

.. _example-spark_on_databricks:

How Flytekit Simplifies Usage of Pyspark in a Users Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The task ``hello_spark`` runs a new spark cluster, which when run locally runs a single node client only cluster,
but when run remote spins up a arbitrarily sized cluster depending on the specified databricks configuration. ``databricks_conf``
The UX is the same as Spark on Kubernetes. Just need to add databricks config to the task config.

"""
import datetime
import random
from operator import add

import flytekit
from flytekit import Resources, task, workflow

# %%
# The following import is required to configure a Spark Server in Flyte:
from flytekitplugins.spark import Spark


# %%
# Spark Task Sample
# ^^^^^^^^^^^^^^^^^
#
# This example shows how a Spark task can be written simply by adding a ``@task(task_config=Spark(...)...)`` decorator.
# Refer to `Spark <https://github.com/flyteorg/flytekit/blob/9e156bb0cf3d1441c7d1727729e8f9b4bbc3f168/plugins/flytekit-spark/flytekitplugins/spark/task.py#L18-L36>`__
# class to understand the various configuration options.
# Databricks Config is equal to the databricks job request.
# Refer to `Databricks job request <https://docs.databricks.com/dev-tools/api/2.0/jobs.html#request-structure>`_
@task(
    task_config=Spark(
        # this configuration is applied to the spark cluster
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
        },
        databricks_conf={
           "run_name": "flytekit databricks plugin example",
           "new_cluster": {
               "spark_version": "11.0.x-scala2.12",
               "node_type_id": "r3.xlarge",
               "aws_attributes": {
                   "availability": "ON_DEMAND",
                   "instance_profile_arn": "arn:aws:iam::590375263360:instance-profile/databricks-s3-role",
               },
               "num_workers": 4,
           },
           "timeout_seconds": 3600,
           "max_retries": 1,
       },
    ),
    limits=Resources(mem="2000M"),
    cache_version="1",
)
def hello_spark(partitions: int) -> float:
    print("Starting Spark with Partitions: {}".format(partitions))

    n = 100000 * partitions
    sess = flytekit.current_context().spark_session
    count = (
        sess.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    )
    pi_val = 4.0 * count / n
    print("Pi val is :{}".format(pi_val))
    return pi_val


def f(_):
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    return 1 if x**2 + y**2 <= 1 else 0


# %%
# This is a regular python function task. This will not execute on the spark cluster
@task(cache_version="1")
def print_every_time(value_to_print: float, date_triggered: datetime.datetime) -> int:
    print("My printed value: {} @ {}".format(value_to_print, date_triggered))
    return 1


# %%
# The workflow shows that a spark task and any python function (or any other task type) can be chained together as long as they match the parameter specifications.
@workflow
def my_spark(triggered_date: datetime.datetime) -> float:
    """
    Using the workflow is still as any other workflow. As image is a property of the task, the workflow does not care
    about how the image is configured.
    """
    pi = hello_spark(partitions=50)
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi


# %%
# Workflows with spark tasks can be executed locally. Some aspects of spark, like links to plugins_hive metastores may not work, but these are limitations of using Spark and are not introduced by Flyte.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running my_spark(triggered_date=datetime.datetime.now()){my_spark(triggered_date=datetime.datetime.now())}"
    )
