"""
Modin vs. Pandas on the ``read_csv`` Function
-------------------------------------------------

In this example, we will see how the Modin plugin helps reduce the time consumed by the ``read_csv`` function to read a huge CSV file (think 10s of GB) into a DataFrame.
We will generate data, invoke the ``read_csv`` function on this data, and compare the time consumed by Modin and pandas.

.. note::

   In this example, we use Ray as the backend.

Installation
^^^^^^^^^^^^^

To install Modin with Ray as the backend,

.. code:: bash

   pip install modin[ray]


To install Modin with Dask as the backend,

.. code:: bash

   pip install modin[dask]

Let's dive into the example.
"""

import ray

ray.shutdown()  # close previous instance of ray
ray.init()  # open a new instance of ray

import time
import typing
from types import ModuleType
from typing import Tuple

# %%
# Next, import the necessary dependencies.
import flytekitplugins.modin
import modin.pandas
import numpy as np
import pandas as pd
from flytekit import task, workflow


# %%
# Data Generation
# ================
#
# Let's define a task to generate data (only once) using the ``random`` method.
@task
def generate_data() -> str:
    df = pd.DataFrame(
        data=np.random.randint(999, 999999, size=(500000, 10)),
        columns=[f"C{i + 1}" for i in range(10)],
    )
    df["C11"] = pd.util.testing.rands_array(5, 500000)
    path = "downloads/data.csv"
    df.to_csv(path)  # 4.18 GB data
    return path


# %%
# Invoke the ``read_csv`` Method Using Pandas and Modin
# ======================================================
#
# Next, we define two tasks that compute the time taken by Pandas and Modin to read a huge CSV file and store it in a Dataframe.
@task
def calculate_time_pandas(my_path: str) -> float:
    start = time.time()
    pandas_df = pd.read_csv(my_path)
    end = time.time()
    pandas_duration = end - start
    return round(pandas_duration, 3)


@task
def calculate_time_modin(my_path: str) -> float:
    start = time.time()
    modin_df = modin.pandas.read_csv(my_path)
    end = time.time()
    modin_duration = end - start
    return round(modin_duration, 3)


# %%
# Compare Time Taken by Modin Versus Pandas
# ==========================================
#
# We compare the time consumed by Modin and Pandas.
@task
def compare_time(time_pandas: float, time_modin: float) -> float:
    time_comparison = time_pandas / time_modin
    return round(time_comparison, 3)


# %%
# Lastly we define a workflow to run the pipeline.
@workflow
def my_workflow(my_path: str) -> float:
    path = generate_data()
    pandas_time = calculate_time_pandas(my_path=path)
    modin_time = calculate_time_modin(my_path=path)
    return compare_time(time_pandas=pandas_time, time_modin=modin_time)


# %%
# Running the Code Locally
# =========================
#
# We can run the code locally too, provided the plugin is set up in the environment.
if __name__ == "__main__":
    result = my_workflow(my_path=generate_data())
    print(
        f"Modin is {my_workflow(my_path = generate_data())} faster than Pandas at `read_csv`"
    )

# %%
# Conclusion
# ^^^^^^^^^^^
#
# We understood how the ``read_csv`` function performs when it is invoked on a Pandas Dataframe and a Modin Dataframe.
# By comparing the time consumed to read a large dataset, we saw that Modin performs better than Pandas.
