"""
03: Conditions
--------------

Flytekit supports conditions as a first class construct in the language. Conditions offer a way to selectively execute branches of a workflow based on static or dynamic data produced by other tasks or come in as workflow inputs.
Conditions are very performant to be evaluated however, they are limited to certain binary and logical operators and can only be performed on primitive values.
"""

# %%
# To start off, import `conditional` module
from flytekit.annotated.condition import conditional

# %%
# Example 1
# In the following example we define two tasks `square` and `double` and depending on whether the workflow input is a fraction (0-1) or not, it decided which to execute.
#
# :py:func:`flytekit.task`
@task()
def square(n: int) -> int:
    """
    Parameters:
        n (int): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer

    Return:
        int: The label for the output will be automatically assigned and type will be deduced from the annotation

    """
    return n*n

# :py:func:`flytekit.task`
@task()
def double(n: int) -> int:
    """
    Parameters:
        n (int): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer

    Return:
        int: The label for the output will be automatically assigned and type will be deduced from the annotation

    """
    return 2*n

@workflow
def multiplier(my_input: int) -> int:
    return conditional("fractions")
        .if_((my_input > 0) & (my_input < 1))
        .then(double(n=my_input))
        .else_(square(n=my_input))

# %%
# Example 2
# In the following example we have an if condition with multiple branches and we fail if no conditions are met. Flyte expects any conditional() statement to be _complete_ meaning all possible branches have to be handled.
@workflow
def multiplier(my_input: int) -> int:
    return conditional("fractions")
        .if_((my_input > 0) & (my_input < 1))
        .then(double(n=my_input))
        .elif_((my_input > 1) & (my_input < 10))
        .then(square(n=my_input))
        .else_()
        .fail("The input must be between 0 and 10")

# %%
# Example 3
# In the following example we consume the output returned by the conditional() in a subsequent task.
@workflow
def multiplier(my_input: int) -> int:
    d = conditional("fractions")
        .if_((my_input > 0) & (my_input < 1))
        .then(double(n=my_input))
        .elif_((my_input > 1) & (my_input < 10))
        .then(square(n=my_input))
        .else_()
        .fail("The input must be between 0 and 10")

    # d will be either the output of `double` or t he output of `square`. If the conditional() falls through the fail branch, execution will not reach here.
    return double(n=d)

# %%
# Example 4
# In the following example we define two tasks with different output interfaces. Flyte will automatically compute the intersection of those outputs and only make those common outputs (based on names and types) available as the final outputs of the `conditional()`.
#
# :py:func:`flytekit.task`
@task()
def sum_div_sub(a: int, b: int) -> typing.NamedTuple("OutputsBC", sum=int, div=int, sub=int):
    return a+b, a/b, a-b

# :py:func:`flytekit.task`
@task()
def sum_sub(a: int, b: int) -> typing.NamedTuple("OutputsBC", sum=int, sub=int):
    return a+b, a-b

@workflow
def math_ops(a: int, b: int) -> (int, int):
    # Flyte will only make `sum` and `sub` available as outputs because they are common between all branches
    sum, sub = conditional("noDivByZero")
                .if_(b == 0)
                .then(sum_sub(a=a, b=b))
                .else_(sum_div_sub(a=a, b=b))

    return sum, sub

# %%
# Example 5
# In the following we define two tasks with completely different output names. Flyte allows what's called output aliases to assign different names to outputs. Doing so allows flyte to know which outputs are common between branches.
#
# :py:func:`flytekit.task`
@task()
def sum_div_sub(a: int, b: int) -> typing.NamedTuple("OutputsBC", summation=int, div=int, subtraction=int):
    return a+b, a/b, a-b

# :py:func:`flytekit.task`
@task()
def sum_sub(a: int, b: int) -> typing.NamedTuple("OutputsBC", sum=int, sub=int):
    return a+b, a-b

@workflow
def math_ops(a: int, b: int) -> (int, int):
    # Flyte will only make `sum` and `sub` available as outputs because they are common between all branches
    sum, sub = conditional("noDivByZero")
                .if_(b == 0)
                .then(sum_sub(a=a, b=b))
                .else_(sum_div_sub(a=a, b=b).with_overrides(aliases={"summation":"sum", "subtraction":"sub"}))

    return sum, sub
