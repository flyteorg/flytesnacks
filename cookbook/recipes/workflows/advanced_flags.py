from flytekit.common.tasks.presto_task import SdkPrestoTask
from flytekit.sdk.tasks import inputs, python_task
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Input, Output

schema = Types.Schema([("a", Types.Integer), ("b", Types.String)])

presto_task = SdkPrestoTask(
    task_inputs=inputs(length=Types.Integer, rg=Types.String),
    statement="SELECT a, chr(a+64) as b from unnest(sequence(1, {{ .Inputs.length }})) t(a)",
    output_schema=schema,
    routing_group="{{ .Inputs.rg }}",
    catalog="hive",  # can be left out if you specify in query
    schema="tmp",  # can be left out if you specify in query
)


@inputs(query_output=Types.Schema())
@python_task
def print_schemas(wf_params, query_output):
    with query_output as r:
        for x in r.iter_chunks():
            df = x.read()
            wf_params.logging.info(f"Output schema:\n{df}")


@workflow_class()
class PrestoWorkflow(object):
    length = Input(Types.Integer, required=True, help="Int between 1 and 26")
    routing_group = Input(Types.String, required=True, help="Test string with no default")
    p_task = presto_task(length=length, rg=routing_group)
    p = print_schemas(query_output=p_task.outputs.results)
    output_a = Output(p_task.outputs.results, sdk_type=schema)


# Workflows can assign a default output location for raw data generated during execution.
raw_output_lp = PrestoWorkflow.create_launch_plan(
    raw_output_data_prefix='s3://lyft-modelbuilder/'
)
