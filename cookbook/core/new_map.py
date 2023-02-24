
@task
def child(a: int):
    ...

@task
def get_data() -> typing.List[int]:
    ...

@task
def get_data_b() -> typing.List[str]:
    ...


@workflow
def wf():
    int_list = get_data()
    str_list = get_data_b()
    constant = 3.14
    cout = tc()
    map_task(child)(a=int_list, b=str_list, c=constant)
    map_task(child)(a=int_list, b=str_list, c=cout)

    map_task(child)(a=int_list)
    map_task(child)(a=int_list)

"""
Partial
3/13-3/17
"""
from functools import partial

@task
def child(a: int, b: str, c: float):
    ...

@task
def pc(a: int, b: str, c: float = 3.14):
    ...


@task
def get_data() -> typing.List[int]:
    ...
@task
def get_data_b() -> typing.List[str]:
    ...


@workflow
def wf():
    int_list = get_data()
    str_list = get_data_b()
    constant = 3.14
    pc = partial(child, c=constant)
    pc2 = partial(child, c=cout)
    map_task(pc)(a=int_list, b=str_list)
