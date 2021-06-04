from flytekit import kwtypes, task, workflow, dynamic

from flytekitplugins.athena import AthenaTask, AthenaConfig
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema

# %%
# This is the world's simplest query. Note that in order for registration to work properly, you'll need to give your
# Athena task a name that's unique across your project/domain for your Flyte installation.
athena_task_no_io = AthenaTask(
    name="sql.athena.no_io",
    inputs={},
    query_template="""
        select 1
    """,
    output_schema_type=None,
    task_config=AthenaConfig(database="mnist"),
)


@workflow
def no_io_wf():
    return athena_task_no_io()


athena_task_w_out = AthenaTask(
    name="sql.athena.w_io",
    inputs=kwtypes(limit=int),
    task_config=AthenaConfig(database="vaccinations"),
    query_template="""
    SELECT * FROM vaccinations limit {{ .inputs.limit }}
    """,
    output_schema_type=FlyteSchema,
)


@task
def print_athena_schema(s: FlyteSchema):
    df = s.open().all()
    print(df.to_markdown())


@workflow
def full_hive_demo_wf(limit: int) -> FlyteSchema:
    demo_schema = athena_task_w_out(limit=limit)
    print_athena_schema(s=demo_schema)
    return demo_schema


