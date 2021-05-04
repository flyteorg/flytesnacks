"""
.. _launch_plans:

Launch Plans
-------------

Launch plans bind a partial or complete list of inputs necessary to launch a workflow, along
with optional run-time overrides such as notifications, schedules and more.
Launch plan inputs must only assign inputs already defined in the reference workflow definition.
"""

import calendar

# %%
# When To Use Launch Plans
# ########################
#
# - For multiple schedules of a workflow with zero or more predefined inputs
# - To run a specific workflow but with a different set of notifications
# - To share a workflow with set inputs with another user, allowing the other user to simply kick off an execution
# - To share a workflow with another user, making sure that some inputs can be overridden if needed
# - To share a workflow with another user, ensuring that some inputs are not changed
#
# Launch plans are the only means for invoking workflow executions.
# A 'default' launch plan will be created during the serialization (and registration process),
# which will optionally bind any default workflow inputs and any default runtime options specified in the project
# flytekit config (such as user role, etc).
#
# The following example creates a default launch plan with no inputs during serialization.
import datetime

from flytekit import LaunchPlan, current_context, task, workflow


@task
def square(val: int) -> int:
    return val * val


@workflow
def my_wf(val: int) -> int:
    result = square(val=val)
    return result


default_lp = LaunchPlan.get_default_launch_plan(current_context(), my_wf)
square_3 = default_lp(val=3)

# %%
# The following shows how to specify a user-defined launch plan that defaults the value of 'val' to 4.
my_lp = LaunchPlan.create("default_4_lp", my_wf, default_inputs={"val": 4})
square_4 = my_lp()
square_5 = my_lp(val=5)

# %%
# It is possible to **fix** launch plan inputs, so that they can't be overridden at execution call time.
my_fixed_lp = LaunchPlan.create("always_2_lp", my_wf, fixed_inputs={"val": 4})
square_2 = my_fixed_lp()
# error:
# square_1 = my_fixed_lp(val=1)

# %%
# Putting It All Together
# #######################
#
# Default and fixed inputs can be used together to simplify individual executions
# and programmatic ones.
# Here is a simple example to greet each day of the upcoming week:


@task
def greet(day_of_week: str, number: int, am: bool) -> str:
    greeting = "Have a great " + day_of_week + " "
    greeting += "morning" if am else "evening"
    return greeting + "!" * number


@workflow
def go_greet(day_of_week: str, number: int, am: bool = False) -> str:
    return greet(day_of_week=day_of_week, number=number, am=am)


morning_greeting = LaunchPlan.create(
    "morning_greeting",
    go_greet,
    fixed_inputs={"am": True},
    default_inputs={"number": 1},
)

# Let's see if we can convincingly pass a Turing test!
today = datetime.datetime.today()
for n in range(7):
    day = today + datetime.timedelta(days=n)
    weekday = calendar.day_name[day.weekday()]
    if day.weekday() < 5:
        print(morning_greeting(day_of_week=weekday))
    else:
        # We're extra enthusiastic on weekends
        print(morning_greeting(number=3, day_of_week=weekday))

# %%
# Partial Inputs for Launch Plans
# ###############################
# Launch plans bind a partial or complete list of inputs necessary to launch a workflow. Launch plan inputs must only assign inputs already defined in the reference workflow definition.  Refer to to :ref:`primary launch plan concept documentation <concepts-launchplans-inputs>` for a detailed introduction to launch plan input types.
#
# For example, for the following workflow definition:

.. code:: python

    from datetime import datetime
    from flytekit import workflow

    @workflow
    def MyWorkflow(region: str, run_date: datetime, sample_size: int=100):
        ...

# To run the workflow over a set of date ranges for a specific region, you could define the following launch plan:

.. code:: python

    from flytekit import LaunchPlan

    sea_launch_plan = LaunchPlan.create(
        "sea_lp",
        MyWorkflow,
        default_inputs={'sample_size': 1000},
        fixed_inputs={'region': 'SEA'},                
    )

# Some things to note here:
# 
# - The ``sample_size`` input is redefined in the launch plan - which is perfectly fine
# - Workflow inputs with default values can be redefined in launch plans
# - ``sample_size`` can also be adjusted at execution creation time because it is possible to override default_inputs in a launch plan
# - It is not possible to override the region input as it is *fixed* 

# The launch plan does not assign run_date, but it is possible to create a launch plan that assigns all workflow inputs (either as default or fixed inputs). The only requirement is that all required inputs 
# without default values must be resolved at execution time. The call to create an execution can still accept inputs
# should your launch plan not define the complete set.

# Backfills With Launch Plans
# ###########################

# This is an example of how to use the launch plan to create executions programmatically to backfill:

.. code:: python

     from datetime import timedelta, date

     run_date = date(2020, 1, 1)
     end_date = date(2021, 1, 1)
     one_day = timedelta(days=1)
     while run_date < end_date:
         sea_launch_plan(run_date=run_date)
         run_date += one_day

# Congratulations! A year's worth of executions have just been created!        
        
