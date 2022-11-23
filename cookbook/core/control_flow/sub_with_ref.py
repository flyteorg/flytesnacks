from flytekit.core.launch_plan import reference_launch_plan
from core.flyte_basics.hello_world import my_wf
from flytekit import workflow


@reference_launch_plan(
    project="flytesnacks",
    domain="development",
    name="core.flyte_basics.hello_world.my_wf",
    version="ref1",
)
def my_wf_lp(
) -> str:
    ...


@workflow
def sub_and_ref():
    lp = my_wf_lp()
    sub = my_wf()
    lp >> sub
