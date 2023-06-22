"""
.. _basics_of_tasks:

=====
Tasks
=====

.. tags:: Basic

Tasks are fundamental building blocks and extension points in Flyte. They possess the following properties:

#. Versioned: Tasks are typically associated with a specific version, often tied to the git sha.
#. Strong Interfaces: Tasks have well-defined inputs and outputs.
#. Declarative: Tasks are defined in a declarative manner.
#. Independently Executable: Tasks can be executed independently.
#. Unit Testable: Tasks can be tested at a unit level.

In Flytekit, tasks can be classified into two types:

- Tasks with an associated Python function: The execution of these tasks is equivalent to executing the associated Python function.
- Tasks without a Python function: These tasks include non-Python functionalities, such as SQL queries, portable tasks like Sagemaker prebuilt algorithms, or services that invoke APIs.

Flyte provides various plugins for tasks, including backend plugins like `Athena <https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-aws-athena/flytekitplugins/athena/task.py>`__.

In this example, we will focus on writing and executing a Python function task.
Additional task types will be addressed in upcoming sections of the integrations guide.
"""
# %%
# Importing the necessary module for any task in Flyte:
from flytekit import task

# %%
# Importing additional modules.
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# %%
# The use of the :py:func:`flytekit.task` decorator is mandatory for a ``PythonFunctionTask``.
# A task is essentially a regular Python function, with the exception that all inputs and outputs must be clearly annotated with their types.
# These types are standard Python types, which will be further explained in the :ref:`type-system section <flytekit_to_flyte_type_mapping>`.
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


# %%
# .. note::
#    Flytekit automatically assigns a default name to the output variable, such as ``out0``.
#    If there are multiple outputs, each output will be numbered starting from 0, for example, ``out0, out1, out2, ...``.
#
# You can execute a Flyte task just like any normal function.
if __name__ == "__main__":
    print(train_model(hyperparameters={"C": 0.1}, test_size=0.2, random_state=42))

# %%
# Invoke a task within a workflow
# ===============================
#
# The primary way to use Flyte tasks is to invoke them in the context of a workflow.
from flytekit import workflow


@workflow
def train_model_wf(
    hyperparameters: dict = {"C": 0.1}, test_size: float = 0.2, random_state: int = 42
) -> LogisticRegression:
    """
    This workflow invokes the train_model task with the given hyperparameters, test size and random state.
    """
    return train_model(
        hyperparameters=hyperparameters, test_size=test_size, random_state=random_state
    )


# %%
# .. note::
#   When invoking the ``train_model`` task, you need to use keyword arguments to specify the values for the corresponding parameters.
#
# Use ``partial`` to provide default arguments to tasks
# =====================================================
#
# You can use the :py:func:`functools.partial` function to assign default or constant values to the parameters of your tasks.
import functools


@workflow
def train_model_wf_with_partial(
    test_size: float = 0.2, random_state: int = 42
) -> LogisticRegression:
    partial_task = functools.partial(train_model, hyperparameters={"C": 0.1})
    return partial_task(test_size=test_size, random_state=random_state)


# %%
# .. _single_task_execution:
#
# .. dropdown:: Execute a single task *without* a workflow
#
#    While workflows are typically composed of multiple tasks with dependencies defined by shared inputs and outputs,
#    there are cases where it can be beneficial to execute a single task in isolation during the process of developing and iterating on its logic.
#    Writing a new workflow definition every time for this purpose can be cumbersome, but executing a single task without a workflow provides a convenient way to iterate on task logic easily.
#
#    To run a task without a workflow, use the following command:
#
#    .. code-block::
#
#       pyflyte run task.py train_model --hyperparameters '{"C": 0.1}' --test_size 0.2 --random_state 42
