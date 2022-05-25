"""
.. _intermediate_spark_dataframes_passing:

Converting a Spark DataFrame to a Pandas DataFrame
==================================================

In this example, you will understand how a Spark dataset can be returned from a task and consumed as a pandas DataFrame.
If the dataframe does not fit in memory, it will result in a runtime failure.
"""

# %%
# Let's import the libraries.
import flytekit
import pandas
from flytekit import Resources, kwtypes, task, workflow
from flytekit.types.structured.structured_dataset import StructuredDataset
from flytekitplugins.spark import Spark

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

# %%
# We define two column types: `name: str` and `age: int`.
columns = kwtypes(name=str, age=int)

# %%
# We define a task that returns a Spark DataFrame.
@task(
    task_config=Spark(
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
        }
    ),
    limits=Resources(mem="2000M"),
    cache_version="1",
)
def create_spark_df() -> Annotated[StructuredDataset, columns]:
    """
    This task returns a Spark dataset that conforms to the defined schema. Failure to do so should result
    in a runtime error. TODO: runtime error enforcement
    """
    sess = flytekit.current_context().spark_session
    return StructuredDataset(
        dataframe=sess.createDataFrame(
            [
                ("Alice", 5),
                ("Bob", 10),
                ("Charlie", 15),
            ],
            ["name", "age"],
        )
    )


# %%
# ``create_spark_df`` is a Spark task that runs within a Spark context (and relies on a Spark cluster that is up and running).
#
# Notice that the task simply returns a ``pyspark.DataFrame`` object, even though the return type specifies ``StructuredDataset``.
# The flytekit type-system will automatically convert the ``pyspark.DataFrame`` to a ``StructuredDataset`` object.
# ``StructuredDataset`` object is an abstract representation of a DataFrame, that can conform to different DataFrame formats.

# %%
# We also define a task that consumes the Spark DataFrame.
@task(cache_version="1")
def sum_of_all_ages(s: Annotated[StructuredDataset, columns]) -> int:
    df: pandas.DataFrame = s.open(pandas.DataFrame).all()
    return int(df["age"].sum())


# %%
# The task ``sum_of_all_ages`` receives a parameter of type ``StructuredDataset``.
# We can use the ``open`` method to specify the DataFrame format, which is ``pandas.DataFrame`` in our case.
# Only performing an ``all`` on structured dataset will load the data into memory (or download if it is run in remote).

# %%
# Finally, we define the workflow.
@workflow
def my_smart_structured_dataset() -> int:
    """
    This workflow shows how a simple schema can be created in Spark and passed to a python function and accessed as a
    pandas DataFrame. Flyte Schemas are abstract DataFrames and not tied to a specific memory representation.
    """
    df = create_spark_df()
    return sum_of_all_ages(s=df)


# %%
# This workflow allows connecting ``create_spark_df`` with ``sum_of_all_ages`` since the return type of the first task and the
# parameter type for the second task match.

# %%
# This program can be executed locally, which greatly simplifies using disparate DataFrame technologies for the end-user.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running my_smart_schema()-> {my_smart_structured_dataset()}")

# %%
# .. note::
#
#    New DataFrame technologies can be dynamically loaded in Flytekit's TypeEngine.
#    To register a custom DataFrame type, you can define an encoder and decoder for ``StructuredDataset`` as outlined in the :ref:`structured_dataset_example` example.
