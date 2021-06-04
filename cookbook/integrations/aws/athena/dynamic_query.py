from flytekit import kwtypes, task, workflow, dynamic
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema

from flytekitplugins.athena import AthenaTask, AthenaConfig

@dataclasses_json
@dataclasses
class Args(object):
    database: str
    inputs_def: Dict[str, Type] = {"x": int}


@dynamic
def generate_and_run_query(path: FlyteFile[".sql"], limit: int, args: Args) -> FlyteSchema:
    with open(path) as f:
        query = f.read()

    athena_task_w_out = AthenaTask(
        name="sql.athena.w_io",
        inputs=args.inputs_def,
        task_config=AthenaConfig(database=args.database),
        query_template=query,
        output_schema_type=FlyteSchema,
    )
    return athena_task_w_out(limit=limit)


@workflow
def athena_output_passing_wf(path: FlyteFile, limit: int, args: Args) -> FlyteSchema:
    return generate_and_run_query(path=path, limit=limit, args=args)


athena_output_passing_wf(path="abc.sql")
athena_output_passing_wf(path="xyz.sql")
