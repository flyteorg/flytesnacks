import random
import datetime
from operator import add
from flytekit import task, Spark, workflow


@task(task_config=Spark(
    spark_conf={
        'spark.driver.memory': "1000M",
        'spark.executor.memory': "1000M",
        'spark.executor.cores': '1',
        'spark.executor.instances': '2',
        'spark.driver.cores': '1',
    }),
    cache_version='1')
def hello_spark(spark_context, partitions: int) -> float:
    print("Starting Spark with Partitions: {}".format(partitions))

    n = 100000 * partitions
    count = spark_context.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
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
    pi = hello_spark(partitions=50)
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running my_spark(triggered_date=datetime.datetime.now()){my_spark(triggered_date=datetime.datetime.now())}")
