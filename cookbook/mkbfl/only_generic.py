"""A simple Flyte example."""

import typing
from typing import List, Optional
from flytekit import task, workflow, map_task
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class Stats:
    frames_count: int = 0
    _shots_per_cluster_count: typing.Union[dict[int, int], None] = None
    face_height_percentiles: typing.Union[list[float], None] = None


@task
def t1(stats: Optional[Stats]) -> Optional[Stats]:
    return stats


@task
def filter_stats(stats: List[Optional[Stats]]) -> List[Stats]:
    return [stat for stat in stats if stat is not None]


@workflow
def wf_stats() -> List[Stats]:
    return filter_stats(
        stats=map_task(t1)(stats=[None, Stats(), Stats(10, {1: 10, 2: 20})]),
    )
