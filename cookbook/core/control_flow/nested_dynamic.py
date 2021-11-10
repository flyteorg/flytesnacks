import typing
from flytekit import dynamic, task, workflow

from core.flyte_basics.lp import default_lp, my_lp, my_wf


@dynamic
def run_lps() -> typing.Tuple[int, int]:
    x = my_lp(val=5)
    y = default_lp(val=7)
    return x, y


@workflow
def run_lps_wf() -> typing.Tuple[int, int]:
    return run_lps()


@workflow
def static_run_lps_wf() -> typing.Tuple[int, int]:
    x = my_lp(val=5)
    y = default_lp(val=7)
    return x, y


@dynamic
def run_subwfs() -> typing.Tuple[int, int]:
    x = my_wf(val=5)
    y = my_wf(val=7)
    return x, y


@workflow
def run_subwfs_wf() -> typing.Tuple[int, int]:
    return run_subwfs()
