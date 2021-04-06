from flytekit import task, workflow, FlyteContext
from flytekit.extend import TypeEngine
from flytekit.types.file import FlyteFile

from flytekit.clients.friendly import SynchronousFlyteClient
from flytekit.models.core.identifier import WorkflowExecutionIdentifier


@task
def task_file_reader():
    client = SynchronousFlyteClient("flyteadmin.flyte.svc.cluster.local:81", insecure=True)
    exec_id = WorkflowExecutionIdentifier(
        domain="development",
        project="flytesnacks",
        name="iaok0qy6k1",
    )
    data = client.get_execution_data(exec_id)
    lit = data.full_outputs.literals["o0"]

    ctx = FlyteContext.current_context()
    ff = TypeEngine.to_python_value(ctx, lv=lit, expected_python_type=FlyteFile)
    with open(ff, 'rb') as fh:
        print(fh.readlines())


@workflow
def tr_example_wf():
    task_file_reader()
