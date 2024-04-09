# Launch plans
from flytekit import LaunchPlan, current_context

# Import the workflow from the workflow.py file
# in order to create a launch plan for it
from .workflow import simple_wf

# Create a default launch plan with no inputs during serialization
default_lp = LaunchPlan.get_default_launch_plan(current_context(), simple_wf)

# Run the launch plan locally
default_lp(x=[-3, 0, 3], y=[7, 4, -2])

# Create a launch plan and specify the default inputs
simple_wf_lp = LaunchPlan.create(
    name="simple_wf_lp", workflow=simple_wf, default_inputs={"x": [-3, 0, 3], "y": [7, 4, -2]}
)

# Trigger the launch plan locally
simple_wf_lp()

# Override the defaults as follows
simple_wf_lp(x=[3, 5, 3], y=[-3, 2, -2])

# It's possible to lock launch plan inputs, preventing them from being overridden during execution
simple_wf_lp_fixed_inputs = LaunchPlan.get_or_create(
    name="fixed_inputs", workflow=simple_wf, fixed_inputs={"x": [-3, 0, 3]}
)
