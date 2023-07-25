from typing import List
from functools import partial
from flytekit import task, workflow, map_task


@task
def t1(name: str, a: List[int]) -> int:
    print(f"{a} and {name}")
    return sum(a)


@workflow
def wf_partial(name: str, wf_list: List[List[int]]) -> List[int]:
    return map_task(partial(t1, name=name))(a=wf_list)


@task
def t2(a: List[int]) -> int:
    print(f"{a}")
    return sum(a)


@workflow
def wf_non_partial(wf_list: List[List[int]]) -> List[int]:
    return map_task(t2)(a=wf_list)


if __name__ == "__main__":
    input_list = [[1, 2, 10], [11, 12]]
    print(f"Running partial workflow {wf_partial(name='test', wf_list=input_list)}")
    # print(f"Running non-partial workflow {wf_non_partial(main=[[1, 2, 10], [11, 12]])}")
