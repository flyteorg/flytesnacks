# %% [markdown]
# (decorating_tasks)=
#
# # Decorating Tasks
#
# ```{eval-rst}
# .. tags:: Intermediate
# ```
#
# You can easily change how tasks behave by using decorators to wrap your task functions.
#
# In order to make sure that your decorated function contains all the type annotation and docstring
# information that Flyte needs, you will need to use the built-in {py:func}`~functools.wraps` decorator.
#
# To begin, import the required dependencies.
# %%
import logging
from functools import partial, wraps

from flytekit import task, workflow

# %% [markdown]
# Create a logger to monitor the execution's progress.
# %%
logger = logging.getLogger(__file__)


# %% [markdown]
# ## Using a single decorator
#
# We define a decorator that logs the input and output details for a decorated task.
# %%
def log_io(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info(f"task {fn.__name__} called with args: {args}, kwargs: {kwargs}")
        out = fn(*args, **kwargs)
        logger.info(f"task {fn.__name__} output: {out}")
        return out

    return wrapper


# %% [markdown]
# We create a task named `t1` that is decorated with `log_io`.
#
# :::{note}
# The order of invoking the decorators is important. `@task` should always be the outer-most decorator.
# :::
# %%
@task
@log_io
def t1(x: int) -> int:
    return x + 1


# %% [markdown]
# (stacking_decorators)=
#
# ## Stacking multiple decorators
#
# You can also stack multiple decorators on top of each other as long as `@task` is the outer-most decorator.
#
# We define a decorator that verifies if the output from the decorated function is a positive number before it's returned.
# If this assumption is violated, it raises a `ValueError` exception.
# %%
def validate_output(fn=None, *, floor=0):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        out = fn(*args, **kwargs)
        if out <= floor:
            raise ValueError(f"output of task {fn.__name__} must be a positive number, found {out}")
        return out

    if fn is None:
        return partial(validate_output, floor=floor)

    return wrapper


# %% [markdown]
# :::{note}
# The output of the `validate_output` task uses {py:func}`~functools.partial` to implement parameterized decorators.
# :::
#
# We define a function that uses both the logging and validator decorators.
# %%
@task
@log_io
@validate_output(floor=10)
def t2(x: int) -> int:
    return x + 10


# %% [markdown]
# Finally, we compose a workflow that calls `t1` and `t2`.
# %%
@workflow
def decorating_task_wf(x: int) -> int:
    return t2(x=t1(x=x))


if __name__ == "__main__":
    print(f"Running decorating_task_wf(x=10) {decorating_task_wf(x=10)}")

# %% [markdown]
# ## Run the example on the Flyte cluster
#
# To run the provided workflow on the Flyte cluster, use the following command:
#
# ```
# pyflyte run --remote \
#   https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/advanced_composition/advanced_composition/decorating_tasks.py \
#   decorating_task_wf --x 10
# ```
#
# In this example, you learned how to modify the behavior of tasks via function decorators using the built-in
# {py:func}`~functools.wraps` decorator pattern. To learn more about how to extend Flyte at a deeper level, for
# example creating custom types, custom tasks or backend plugins,
# see {ref}`Extending Flyte <plugins_extend>`.
