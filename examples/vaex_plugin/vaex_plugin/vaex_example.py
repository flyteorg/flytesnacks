# %% [markdown]
# # VaexDataframe Example
#
# In this example, we will see how to leverage VaexDataframeRenderer to visualize and explore big dataframes.
#
# :::{note}
# The provider source code can be found in the [flytekit-vaex tests](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-vaex/tests/test_vaex_plugin_sd.py) which is inside flytekit plugins.
# :::
# First, import the necessary libraries.
# %%
import pandas as pd
import vaex
from flytekitplugins.vaex.sd_transformers import VaexDataFrameRenderer
from typing_extensions import Annotated

from flytekit import kwtypes, task, workflow
from flytekit.types.structured.structured_dataset import PARQUET, StructuredDataset
