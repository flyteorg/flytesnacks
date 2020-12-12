"""
This example shows how users can return a spark.Dataset from a task and consume it as a pandas.DataFrame.
If the dataframe does not fit in memory, it will result in a runtime failure.
"""
import flytekit
import pandas
from flytekit import task, workflow, kwtypes
from flytekit.taskplugins.spark import Spark
from flytekit.types import FlyteSchema

"""
This section defines a simple schema type with 2 columns, `name: str` and `age: int`
"""
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
    """
    This spark program returns a spark dataset that conforms to the defined schema. Failure to do so should result
    in a runtime error. TODO: runtime error enforcement
    """
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
    """
    The schema is passed into this task. Schema is just a reference to the actually object and has almost no overhead.
    Only performing an ``open`` on the schema will cause the data to be loaded into memory (also downloaded if this being
    run in a remote setting)
    """
    # This by default returns a pandas.DataFrame object. ``open`` can be parameterized to return other dataframe types
    reader = s.open()
    # supported dataframes
    df: pandas.DataFrame = reader.all()
    return df['age'].sum()


@workflow
def my_smart_schema() -> int:
    """
    This workflow shows how a simple schema can be created in spark and passed to a python function and accessed as a
    pandas.DataFrame. Flyte Schemas are abstract data frames and not really tied to a specific memory representation.
    """
    df = create_spark_df()
    return sum_of_all_ages(s=df)


if __name__ == "__main__":
    """
    This program can be run locally
    """
    print(f"Running {__file__} main...")
    print(f"Running my_smart_schema()-> {my_smart_schema()}")
