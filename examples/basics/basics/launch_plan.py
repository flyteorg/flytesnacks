from flytekit import LaunchPlan, current_context
from .workflow import simple_wf

default_lp = LaunchPlan.get_default_launch_plan(current_context(), simple_wf)
default_lp(x=[-3, 0, 3], y=[7, 4, -2])


simple_wf_lp = LaunchPlan.create(
    name="simple_wf_lp", workflow=simple_wf, default_inputs={"x": [-3, 0, 3], "y": [7, 4, -2]}
)

simple_wf_lp()

simple_wf_lp(x=[3, 5, 3], y=[-3, 2, -2])

simple_wf_lp_fixed_inputs = LaunchPlan.get_or_create(
    name="fixed_inputs", workflow=simple_wf, fixed_inputs={"x": [-3, 0, 3]}
)
