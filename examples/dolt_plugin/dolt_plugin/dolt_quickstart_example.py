# %% [markdown]
# # Quickstart
#
# In this demo and following example, learn how to use `DoltTable` to annotate DataFrame inputs and outputs in the Flyte tasks.
#
# ```{eval-rst}
# .. youtube:: TfBIuHYkyvU
#
# ```
# %% [markdown]
# First, let's import the libraries.
# %%
import sys
from pathlib import Path

import pandas as pd
from flytekit import task, workflow
from flytekitplugins.dolt.schema import DoltConfig, DoltTable

# %% [markdown]
# Next, we initialize Dolt's config.
# %%
doltdb_path = str(Path(__file__).parent / "foo")

rabbits_conf = DoltConfig(
    db_path=doltdb_path,
    tablename="rabbits",
)


# %% [markdown]
# We define a task to create a DataFrame and store the table in Dolt.


# %%
@task
def populate_rabbits(a: int) -> DoltTable:
    rabbits = [("George", a), ("Alice", a * 2), ("Sugar Maple", a * 3)]
    df = pd.DataFrame(rabbits, columns=["name", "count"])
    return DoltTable(data=df, config=rabbits_conf)


# %% [markdown]
# `unwrap_rabbits` task does the exact opposite -- reading the table from Dolt and returning a DataFrame.
# %%
@task
def unwrap_rabbits(table: DoltTable) -> pd.DataFrame:
    return table.data


# %% [markdown]
# Our workflow combines the above two tasks:
# %%
@workflow
def wf(a: int) -> pd.DataFrame:
    rabbits = populate_rabbits(a=a)
    df = unwrap_rabbits(table=rabbits)
    return df


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    if len(sys.argv) != 2:
        raise ValueError("Expected 1 argument: a (int)")
    a = int(sys.argv[1])
    result = wf(a=a)
    print(f"Running wf(), returns dataframe\n{result}\n{result.dtypes}")

# %% [markdown]
# Run this task by issuing the following command:
#
# ```{eval-rst}
# .. prompt:: $
#
#   python quickstart_example.py 1
# ```
#
