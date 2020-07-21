from flytekit.sdk.tasks import python_task, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import Input


@inputs(in_time=Types.Datetime)
@python_task
def print_time(wf_params, in_time):
    print("{}".format(in_time))


class ScheduledWorkflow():
    trigger_time = Input(Types.Datetime, required=True)  # Time at which the workflow was scheduled
    print_time(in_time=trigger_time)
