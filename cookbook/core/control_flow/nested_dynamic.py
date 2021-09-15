import typing
from flytekit import dynamic, task, workflow

from cookbook.core.flyte_basics.lp import default_lp, my_lp


@dynamic
def run_lps() -> typing.Tuple[int, int]:
    x = my_lp(val=5)
    y = default_lp(val=7)
    return x, y


@workflow
def run_lps_wf() -> typing.Tuple[int, int]:
    return run_lps()
