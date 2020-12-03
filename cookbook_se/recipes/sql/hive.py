from flytekit import workflow, kwtypes, task
from flytekit.taskplugins.hive import HiveTask, HiveSelectTask
from flytekit.types.schema import FlyteSchema


hive_task_no_io = HiveTask(
    name="recipes.sql.hive.no_io",
    inputs={},
    cluster_label="flyte",
    query_template="""
        select 1
    """,
    output_schema_type=None,
)


@workflow
def no_io_wf():
    return hive_task_no_io()


hive_task_w_out = HiveTask(
    name="recipes.sql.hive.w_out",
    inputs={},
    cluster_label="flyte",
    query_template="""
    CREATE TEMPORARY TABLE {{ .PerRetryUniqueKey }}_tmp AS select 1;
    CREATE EXTERNAL TABLE {{ .PerRetryUniqueKey }} LIKE {{ .PerRetryUniqueKey }}_tmp STORED AS PARQUET;
    ALTER TABLE {{ .PerRetryUniqueKey }} SET LOCATION '{{ .RawOutputDataPrefix }}';

    INSERT OVERWRITE TABLE {{ .PerRetryUniqueKey }}
        SELECT *
        FROM {{ .PerRetryUniqueKey }}_tmp;
    DROP TABLE {{ .PerRetryUniqueKey }};
    """,
    output_schema_type=FlyteSchema
)


@workflow
def with_output_wf() -> FlyteSchema:
    return hive_task_w_out()


demo_all = HiveSelectTask(
    name="recipes.sql.hive.demo_all",
    inputs=kwtypes(ds=str, earlier_schema=FlyteSchema),
    cluster_label="flyte",
    select_query="""
    SELECT '.PerRetryUniqueKey' as template_key, '{{ .PerRetryUniqueKey }}' as template_value 
    UNION
    SELECT '.RawOutputDataPrefix' as template_key, '{{ .RawOutputDataPrefix }}' as template_value
    UNION
    SELECT '.inputs.earlier_schema' as template_key, '{{ .inputs.earlier_schema }}' as template_value
    UNION
    SELECT '.inputs.ds' as template_key, '{{ .inputs.ds }}' as template_value
    """,
    output_schema_type=FlyteSchema
)


@task
def print_schema(s: FlyteSchema):
    df = s.open().all()
    print(df.to_markdown())


@workflow
def full_hive_demo_wf() -> FlyteSchema:
    s = hive_task_w_out()
    demo_schema = demo_all(ds="2020-01-01", earlier_schema=s)
    print_schema(s=demo_schema)
    return demo_schema
