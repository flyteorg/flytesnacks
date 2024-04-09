from typing import Tuple

from flytekit import workflow

# Import the `slope` and `intercept` tasks from the `workflow.py` file.
from .workflow import intercept, slope


# Sphinx-style docstring
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


# NumPy-style docstring
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


# Google-style docstring
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
