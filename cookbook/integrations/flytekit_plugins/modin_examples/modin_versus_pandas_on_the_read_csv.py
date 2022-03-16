"""
Modin versus Pandas on the ``read_csv`` Function
-------------------------------------------------

In this example, we will see how the Modin plugin helps reduce the time consumed by the ``read_csv`` function to read a huge CSV file (think 10s of GB) into a Pandas Dataframe.

The striking feature of Modin is that a single line of code can speed up the operation by up to 4 times.
We will generate the data and invoke the ``read_csv`` function on this data. We will use Modin and Pandas to read the Dataframe and compare the time consumed.

.. note::

   Here, we use Ray as the backend.

"""
# %%
# First, let's import all the necessary dependencies.
import ray
ray.shutdown() # to close previous instance of ray
ray.init() # to open a new instance of ray
import modin.pandas as pd
import time
import numpy as np
import pandas as old_pd
import typing
from typing import Tuple
from types import ModuleType
from flytekit import task, workflow

# %%
# Data Generation
# ================
#
# Let's generate data (only once) using the ``random`` method.
df = old_pd.DataFrame(data=np.random.randint(999, 999999, size=(50000000,10)),columns=['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10'])
df['C11'] = old_pd.util.testing.rands_array(5,50000000)
df.to_csv("huge_data.csv") # 4.18 GB data
path = "huge_data.csv"


# %%
# Task to Invoke the ``read_csv`` Method Using Pandas 
# ==================================================
#
# Now, let us define a task that computes the time taken by Pandas to read a huge CSV file and store it in a Dataframe.
@task
def calculate_time_pandas(my_path:str)-> float:
    start = time.time()
    pandas_df = old_pd.read_csv(my_path)
    end = time.time()
    pandas_duration = end - start
    return (round(pandas_duration, 3))
    #return pandas_duration
 
# %%
# Task to Invoke the ``read_csv`` Method Using Modin 
# ==================================================
#
# Next, let us define a task that computes the time taken by Modin to read a huge CSV file and store it in a Dataframe.
@task
def calculate_time_modin(my_path: str)-> float:
    start = time.time()
    modin_df = pd.read_csv(my_path)
    end = time.time()
    modin_duration = end - start
    return (round(modin_duration, 3))

# %%
# Task to Compare Time Taken by Modin Versus Pandas 
# ==================================================
# 
# We define a task to compare the time consumed by Modin and Pandas.
@task
def compare_time(time_1: float, time_2: float)-> float:
    time_speed = time_1/time_2
    return (round(time_speed, 3))

# %%
# Lastly we define a workflow to run the pipeline.
@workflow
def my_workflow(my_path: str) -> float:
    pandas_time = calculate_time_pandas(my_path = path)
    modin_time = calculate_time_modin(my_path = path)
    return compare_time(time_1=pandas_time, time_2=modin_time)

# %%
# Running the Code Locally
# =========================
#
# We can run the code locally too, provided the plugin is set up in the environment.
if __name__ == "__main__":
    result = my_workflow(my_path = path)
    #print("Modin v/s Pandas time: ",result)
    print("Modin is {} x faster than Pandas at `read_csv`".format(result))
