"""
This Example shows how to write is task in flytekit python.
Recap: In Flyte a task is a fundamental building block and an extension point. Flyte has multiple plugins for tasks,
which can be either a backend-plugin or can be a simple extension that is available in flytekit.

A task in flytekit can be 2 types
 1. A task that has a python function associated with it. The execution of the task would be an execution of this function
 2. a task that does not have a python function, for e.g a SQL query or some other portable task like Sagemaker prebuilt
    algorithms, or something that just invokes an API

This section will talk about how to write a Python Function task. Other type of tasks will be covered in later sections

"""

from flytekit import task


@task
def square(n: int) -> int:
    """
    A ``PythonFunctionTask`` must always be decorated with the ``@task`` ``flytekit.task`` decorator.
    The task itself is a regular python function, with one exception, it needs all the inputs and outputs to be clearly
    annotated with the types. The types are regular python types, more on this in the type-system section.

    .. code-block:: python

        from flytekit import task

        @task
        def my_task(x: int) -> int:
          ...

    Parameters:
        n (int): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer

    Return:
        int: The label for the output will be automatically assigned and type will be deduced from the annotation

    In this task, one input is ``n`` which has type ``int``.
    the task ``square`` takes the number ``n`` and returns a new integer (squared value)

    Flytekit will assign a default name to the output variable like ``out0`` (TODO: rename to ``o0``)

    In case of multiple outputs, each output will be numbered in the order starting with 0. For e.g. -> o0, o1, o2, ...
    """
    return n*n


