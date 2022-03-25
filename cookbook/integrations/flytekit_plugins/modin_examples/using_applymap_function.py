"""
Using ``applymap`` Function
----------------------------

In this example, we will see how the Modin Dataframe works with :ref:`tasks <divedeep-tasks>` and :ref:`workflows <divedeep-workflows>` for the ``applymap`` function.
We will generate data, and store it in a Modin Dataframe. We will invoke the ``applymap`` function on this dataframe.

"""

# %%
# Import ``ray`` and close the previous instances (if any) and start a new instance.
import ray
ray.shutdown() # close previous instance of ray
ray.init() # open a new instance of ray

# %%
# Next, import the necessary dependencies.
import flytekitplugins.modin
import modin.pandas
import time
import numpy as np
import pandas as pd
import typing
from typing import Tuple
from types import ModuleType
from flytekit import task, workflow

# %%
# Data Generation
# ================
#
# Let's define a task to generate data (only once) using the ``random`` method. This data is stored in a Modin Dataframe.
@task
def generate_data() -> modin.pandas.DataFrame:
    df = modin.pandas.DataFrame(data=np.random.randint(999, 999999, size=(300000,4)),columns=[f'C{i + 1}' for i in range(4)])
    return df

 
# %%
# Invoke the ``applymap`` Method 
# ===============================
#
# Next, let us define a task that invokes the ``applymap`` method on the Modin Dataframe.
@task
def modin_applymap_function_usage(my_input: modin.pandas.DataFrame)-> modin.pandas.DataFrame:
    modin_df = my_input.applymap(lambda x: x%2)
    return modin_df

# %%
# Lastly we define a workflow to run the pipeline.
@workflow
def my_workflow(my_input: modin.pandas.DataFrame) -> modin.pandas.DataFrame:
    return modin_applymap_function_usage(my_input = generate_data())

# %%
# Running the Code Locally
# =========================
#
# We can run the code locally too, provided the plugin is set up in the environment.
if __name__ == "__main__":
    my_data = generate_data()
    result = my_workflow(my_input = my_data)
    print(result)


# %%
# Conclusion
# ^^^^^^^^^^^
#
# We understood how Modin Dataframe invokes the ``applymap`` function using tasks and workflows in Flyte.
