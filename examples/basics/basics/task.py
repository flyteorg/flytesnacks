# %% [markdown]
# (basics_of_tasks)=
#
# # Tasks
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Task is a fundamental building block and an extension point of Flyte, which 
# encapsulates the users' code. They possess the following properties:
#
# 1. Versioned (usually tied to the `git revision`)
# 2. Strong interfaces (specified inputs and outputs)
# 3. Declarative
# 4. Independently executable
# 5. Unit testable
#
# A task in Flytekit can be of two types:
#
# 1. A task that has a Python function associated with it. The execution of the 
#    task is equivalent to the execution of this function.
# 2. A task that doesn't have a Python function, e.g., an SQL query or any 
#    portable task like Sagemaker prebuilt algorithms, or a service that 
#    invokes an API.
#
# Multiple plugins for tasks--including backend plugins--are available in Flyte.
# See also ([Athena](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-aws-athena/flytekitplugins/athena/task.py)).
#
# In this example, you will learn how to write and execute a `Python function task`. 
# Other types of tasks are covered in the later sections.
# %% [markdown]
# For any task in Flyte, there is one necessary import, which is:
# %%
from flytekit import task

# %%
# Importing additional modules.
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# %% [markdown]
# The use of the {py:func}`flytekit.task` decorator is mandatory for
# a ``PythonFunctionTask``.
# A task is a regular Python function, but with a requirement that
# all inputs and outputs must be clearly annotated with their types.
# These types are standard Python types, which are further explained
# in the {ref}`type-system section <flytekit_to_flyte_type_mapping>`.


# %%
@task
def train_model(
    hyperparameters: dict, test_size: float, random_state: int
) -> LogisticRegression:
    """
    Parameters:
        hyperparameters (dict): A dictionary containing the hyperparameters for the model.
        test_size (float): The proportion of the data to be used for testing.
        random_state (int): The random seed for reproducibility.

    Return:
        LogisticRegression: The trained logistic regression model.
    """
    # Loading the Iris dataset
    iris = load_iris()

    # Splitting the data into train and test sets
    X_train, _, y_train, _ = train_test_split(
        iris.data, iris.target, test_size=test_size, random_state=random_state
    )

    # Creating and training the logistic regression model with the given hyperparameters
    clf = LogisticRegression(**hyperparameters)
    clf.fit(X_train, y_train)

    return clf


# %% [markdown]
# :::{note}
# Flytekit will assign a default name to the output variable like `out0`.
# In case of multiple outputs, each output will be numbered in the order
# starting with 0, e.g., -> `out0, out1, out2, ...`.
# :::
#
# You can execute a Flyte task as any normal function.
# %%
if __name__ == "__main__":
    print(
        train_model(hyperparameters={"C": 0.1}, test_size=0.2, random_state=42)
    )

# %% [markdown]
# ## Invoke a Task within a Workflow
#
# The primary way to use Flyte tasks is to invoke them in the context of a workflow.

# %%
from flytekit import workflow


@workflow
def train_model_wf(
    hyperparameters: dict = {"C": 0.1},
    test_size: float = 0.2,
    random_state: int = 42,
) -> LogisticRegression:
    """
    This workflow invokes the train_model task with the given hyperparameters,
    test size and random state.
    """
    return train_model(
        hyperparameters=hyperparameters,
        test_size=test_size,
        random_state=random_state,
    )


# %% [markdown]
# ```{note}
# When invoking the `train_model` task, you need to use keyword arguments to 
# specify the values for the corresponding parameters.
# ````
#
# ## Use `partial` to provide default arguments to tasks
#
# You can use the {py:func}`functools.partial` function to assign default or 
# constant values to the parameters of your tasks.

# %%
import functools


@workflow
def train_model_wf_with_partial(
    test_size: float = 0.2, random_state: int = 42
) -> LogisticRegression:
    partial_task = functools.partial(train_model, hyperparameters={"C": 0.1})
    return partial_task(test_size=test_size, random_state=random_state)


# %% [markdown]
# (single_task_execution)=
#
# :::{dropdown} Execute a single task *without* a workflow
#
# While workflows are typically composed of multiple tasks with dependencies 
# defined by shared inputs and outputs, there are cases where it can be beneficial 
# to execute a single task in isolation during the process of developing and 
# iterating on its logic. Writing a new workflow definition every time for this 
# purpose can be cumbersome, but executing a single task without a workflow 
# provides a convenient way to iterate on task logic easily.
#
# To run a task without a workflow, use the following command:
#
# ```{code-block}
# pyflyte run task.py train_model --hyperparameters '{"C": 0.1}' --test_size 0.2 --random_state 42
# ```
# :::
