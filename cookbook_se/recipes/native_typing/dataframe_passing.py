import datetime
import random

import flytekit
import pandas
from flytekit import task, workflow, kwtypes
from flytekit.taskplugins.spark import Spark
from flytekit.types import FlyteSchema

my_schema = FlyteSchema[kwtypes(name=str, age=int)]


@task(task_config=Spark(
    spark_conf={
        'spark.driver.memory': "1000M",
        'spark.executor.memory': "1000M",
        'spark.executor.cores': '1',
        'spark.executor.instances': '2',
        'spark.driver.cores': '1',
    }),
    cache_version='1',
    container_image='{{.image.default.fqn}}:spark-{{.image.default.version}}')
def create_spark_df() -> my_schema:
    sess = flytekit.current_context().spark_session
    return sess.createDataFrame(
        [
            ("Alice", 5),
            ("Bob", 10),
            ("Charlie", 15),
        ],
        my_schema.column_names(),
    )


@task(cache_version='1')
def sum_of_all_ages(s: my_schema) -> int:
    # This by default returns a pandas.DataFrame object. ``open`` can be parameterized to return other dataframe types
    reader = s.open()
    # supported dataframes
    df: pandas.DataFrame = reader.all()
    return df['age'].sum()


@workflow
def my_smart_schema() -> int:
    df = create_spark_df()
    return sum_of_all_ages(s=df)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running my_smart_schema()-> {my_smart_schema()}")
