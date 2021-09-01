from __future__ import absolute_import, division, print_function

import typing

from flytekit import task, workflow, dynamic


@task(cache_version="1.0", cache=True)
def my_maybe_cached_task(seed: int, index: int) -> int:
    return seed + index


@dynamic
def my_dynamic_task(seed: int) -> typing.List[int]:
    for x in range(1, 10):
        o = my_maybe_cached_task(seed=seed, index=x)

    return [1, 2, 3]


@workflow
def compute_average_workflow(
    seed: int
) -> typing.List[int]:
    return my_dynamic_task(seed=seed)
