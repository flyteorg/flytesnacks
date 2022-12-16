from random import random

import flytekit
from operator import add

from flytekit import task, workflow
from flytekitplugins.spark import Spark


@task
def t1(partitions: int) -> int:
    return partitions


databricks_conf = {
    "run_name": "flytekit databricks plugin example",
    "new_cluster": {
        "spark_version": "11.0.x-scala2.12",
        "node_type_id": "r3.xlarge",
        "aws_attributes": {
            "availability": "ON_DEMAND",
            "instance_profile_arn": "arn:aws:iam::590375264460:instance-profile/databricks-s3-role",
        },
        "num_workers": 4,
    },
    "timeout_seconds": 3600,
    "max_retries": 1,
}


@task(task_config=Spark(databricks_conf=databricks_conf))
def my_spark(partitions: int) -> float:
    n = 1000 * partitions

    def f(_: int) -> float:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    spark = flytekit.current_context().spark_session
    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    pi = 4.0 * count / n
    print("Pi is roughly %f" % pi)
    return pi


@workflow
def my_wf(partitions: int = 5):
    res = t1(partitions=partitions)
    my_spark(partitions=res)


# pyflyte -c ~/.flyte/config-sandbox.yaml register --image pingsutw/flyte-app:abc123 --destination-dir . \
#   --version dbtst_yt4 integrations/external_services/dbricks.py
if __name__ == "__main__":
    my_wf()
