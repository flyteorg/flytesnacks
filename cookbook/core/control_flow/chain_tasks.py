"""
Chain Flyte Tasks
-----------------

Data passing between tasks need not necessarily happen through parameters.
Flyte provides a mechanism to chain tasks using the ``>>`` operator and the ``create_node`` function.
You may want to call this function to specify dependencies between tasks that don't consume or produce outputs.

Let's use this example to impose ``read()`` order after ``write()``.
"""
# %%
import pandas as pd

# %%
# First, import the necessary dependencies.
from flytekit import task, workflow
from flytekit.core.node_creation import create_node

DATABASE = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
# %%
# Define a ``read()`` task to read from the file.
@task
def read() -> pd.DataFrame:
    data = pd.read_csv(DATABASE)
    return data

# %%
# Define a ``write()`` task to write to the file. Let's assume we are populating the CSV file.
@task
def write():
    # dummy code
    df = pd.DataFrame(  # noqa : F841
        data={
            "sepal_length": [5.3],
            "sepal_width": [3.8],
            "petal_length": [0.1],
            "petal_width": [0.3],
            "species": ["setosa"],
        }
    )

    # Write the data to a database
    # pd.to_csv("...")
# %%
# We want to enforce an order here: ``write()`` followed by ``read()``. Since no data-passing happens between the tasks, we use ``>>`` operator on the nodes.

@workflow
def chain_tasks_wf() -> pd.DataFrame:
    write_node = create_node(write)
    read_node = create_node(read)

    write_node >> read_node

    return read_node.o0
# %%
# .. note::
#   To send arguments while creating a node, use the following syntax:
#
#   .. code-block:: python
#
#       create_node(task_name, parameter1=argument1, parameter2=argument2, ...)

# %% 
# How to chain SubWorkflows?
# ^^^^^^^^^^^^^^^^^^^^^^^^
# 
# Similar to tasks, you can also chain `Subworkflows <https://docs.flyte.org/projects/cookbook/en/latest/auto/core/control_flow/subworkflows.html>`_ as follows:

# %% 
# First, define a sub workflow for ``write()``.

@workflow
def write_sub_workflow():
    write()


# %%
# Then define a sub workflow for ``read()``.
@workflow
def read_sub_workflow() -> pd.DataFrame:
    return read()

#  %%
# Use ``>>`` operator on the nodes to chain subworkflows.
@workflow
def chain_workflows_wf() -> pd.DataFrame:
    write_sub_wf = write_sub_workflow()
    read_sub_wf = read_sub_workflow()

    write_sub_wf >> read_sub_wf

    return read_sub_wf
#%%
# Finally, run the workflow locally.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running chain_tasks_wf()... {chain_tasks_wf()}")
    print(f"Running chain_workflows_wf()... {chain_workflows_wf()}")