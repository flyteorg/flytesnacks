import typing
from random import random
from flytekit import task, workflow, conditional, Resources


@task(limits=Resources(mem="1Gi", cpu="1"))
def none_func() -> typing.Optional[str]:
    return f"the input is None"


@task(limits=Resources(mem="1Gi", cpu="1"))
def not_none_func(obj) -> str:
    return f"the input {obj} is not None"


@task(limits=Resources(mem="1Gi", cpu="1"))
def get_none() -> typing.Optional[str]:
    return None


@task(limits=Resources(mem="1Gi", cpu="1"))
def get_int() -> typing.Optional[int]:
    if random() > 0.5:
        return None

    return 100


@workflow
def none_wf2() -> typing.Optional[str]:
    my_input = get_int()

    return (
        conditional("testing_none")
        .if_(my_input == None)
        .then(none_func())
        .else_()
        .then(not_none_func(obj=my_input))
    )


if __name__ == "__main__":
    none_wf2()
