from __future__ import absolute_import
from __future__ import print_function


from flytekit.sdk.tasks import inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Input, Output
from flytekit.common.tasks.presto_task import SdkPrestoTask
from flytekit.models.common import RawOutputDataConfig

schema = Types.Schema([("a", Types.Integer), ("b", Types.String)])

presto_task = SdkPrestoTask(
    task_inputs=inputs(length=Types.Integer, rg=Types.String),
    statement="SELECT a, chr(a+64) as b from unnest(sequence(1, {{ .Inputs.length }})) t(a)",
    output_schema=schema,
    routing_group="{{ .Inputs.rg }}",
    catalog="hive",  # can be left out if you specify in query
    schema="tmp",  # can be left out if you specify in query
)


@workflow_class()
class CustomRawOutputWorkflow(object):
    length = Input(Types.Integer, required=True, help="Int between 1 and 26")
    routing_group = Input(Types.String, required=True, help="Test string with no default")
    p_task = presto_task(length=length, rg=routing_group)
    output_a = Output(p_task.outputs.results, sdk_type=schema)


# Workflows can assign a default output location for raw data generated during execution.
raw_output_lp = CustomRawOutputWorkflow.create_launch_plan(
    raw_output_data_config=RawOutputDataConfig("s3://test-raw-bucket/")
)