from flytekit import task, workflow, eager


# Example 1
@task
def add_one(x: int) -> int:
    return x + 1


@task
def double(x: int) -> int:
    return x * 2


@eager
async def simple_eager_workflow(x: int) -> int:
    out = add_one(x=x)
    if out < 0:
        return -1
    return double(x=out)


# Example 2
@eager
async def another_eager_workflow(x: int) -> int:
    out = add_one(x=x)

    # out is a Python integer
    out = out - 1

    return double(x=out)


# Example 3
@task
def gt_100(x: int) -> bool:
    return x > 100


@eager
async def eager_workflow_with_conditionals(x: int) -> int:
    out = add_one(x=x)

    if out < 0:
        return -1
    elif gt_100(x=out):
        return 100
    else:
        out = double(x=out)

    assert out >= -1
    return out


# Example 4
# Gather the outputs of multiple tasks or subworkflows into a list:
import asyncio

@task
async def add_one_async(x: int) -> int:
    return x + 1


@eager
async def eager_workflow_with_for_loop(x: int) -> int:
    outputs = []

    for i in range(x):
        outputs.append(add_one_async(x=i))

    outputs = await asyncio.gather(*outputs)
    return double(x=sum(outputs))


# Example 5
# Static subworkflows
@workflow
def subworkflow(x: int) -> int:
    out = add_one(x=x)
    return double(x=out)


@eager
async def eager_workflow_with_static_subworkflow(x: int) -> int:
    out = subworkflow(x=x)
    assert out == (x + 1) * 2
    return out


# Example 6
# Nested eager tasks
@eager
async def eager_subworkflow(x: int) -> int:
    return add_one(x=x)


@eager
async def nested_eager_workflow(x: int) -> int:
    out = await eager_subworkflow(x=x)
    return double(x=out)


# Example 7
# Catching exceptions
from flytekit.exceptions.eager import EagerException


@task
def raises_exc(x: int) -> int:
    if x <= 0:
        raise TypeError
    return x


@eager
async def eager_workflow_with_exception(x: int) -> int:
    try:
        return await raises_exc(x=x)
    except EagerException:
        return -1


# Execute eager workflows locally by calling them
# like a regular `async` function

if __name__ == "__main__":
    result = asyncio.run(simple_eager_workflow(x=5))
    print(f"Result: {result}")  # "Result: 12"
