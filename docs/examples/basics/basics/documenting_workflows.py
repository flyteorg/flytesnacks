# %% [markdown]
# # Documenting Workflows
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Well-documented code significantly improves code readability.
# Flyte enables the use of docstrings to document your code.
# Docstrings are stored in [FlyteAdmin](https://docs.flyte.org/en/latest/concepts/admin.html)
# and displayed on the UI.
#
# To begin, import the relevant libraries.
# %%
from typing import Tuple

from flytekit import workflow

# %% [markdown]
# We import the `slope` and `intercept` tasks from the `workflow.py` file.
# %%
from .workflow import intercept, slope


# %% [markdown]
# ## Sphinx-style docstring
#
# An example to demonstrate Sphinx-style docstring.
#
# The initial section of the docstring provides a concise overview of the workflow.
# The subsequent section provides a comprehensive explanation.
# The last part of the docstring outlines the parameters and return type.
# %%
@workflow
def sphinx_docstring_wf(x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]) -> Tuple[float, float]:
    """
    Slope and intercept of a regression line

    This workflow accepts a list of coefficient pairs for a regression line.
    It calculates both the slope and intercept of the regression line.

    :param x: List of x-coefficients
    :param y: List of y-coefficients
    :return: Slope and intercept values
    """
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return slope_value, intercept_value


# %% [markdown]
# ## NumPy-style docstring
#
# An example to demonstrate NumPy-style docstring.
#
# The first part of the docstring provides a concise overview of the workflow.
# The next section offers a comprehensive description.
# The third section of the docstring details all parameters along with their respective data types.
# The final section of the docstring explains the return type and its associated data type.
# %%
@workflow
def numpy_docstring_wf(x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]) -> Tuple[float, float]:
    """
    Slope and intercept of a regression line

    This workflow accepts a list of coefficient pairs for a regression line.
    It calculates both the slope and intercept of the regression line.

    Parameters
    ----------
    x : list[int]
        List of x-coefficients
    y : list[int]
        List of y-coefficients

    Returns
    -------
    out : Tuple[float, float]
        Slope and intercept values
    """
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return slope_value, intercept_value


# %% [markdown]
# ## Google-style docstring
#
# An example to demonstrate Google-style docstring.
#
# The initial section of the docstring offers a succinct one-liner summary of the workflow.
# The subsequent section of the docstring provides an extensive explanation.
# The third segment of the docstring outlines the parameters and return type,
# including their respective data types.
# %%
@workflow
def google_docstring_wf(x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]) -> Tuple[float, float]:
    """
    Slope and intercept of a regression line

    This workflow accepts a list of coefficient pairs for a regression line.
    It calculates both the slope and intercept of the regression line.

    Args:
      x (list[int]): List of x-coefficients
      y (list[int]): List of y-coefficients

    Returns:
      Tuple[float, float]: Slope and intercept values
    """
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return slope_value, intercept_value


# %% [markdown]
# Here are two screenshots showcasing how the description appears on the UI:
# 1. On the workflow page, you'll find the short description:
# :::{figure} https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/document_wf_short.png
# :alt: Short description
# :class: with-shadow
# :::
#
# 2. If you click into the workflow, you'll see the long description in the basic information section:
# :::{figure} https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/document_wf_long.png
# :alt: Long description
# :class: with-shadow
# :::
