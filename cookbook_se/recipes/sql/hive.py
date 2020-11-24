from flytekit import workflow
from flytekit.taskplugins.hive.task import HiveTask
from flytekit.types.schema import FlyteSchema


default_select_template = """
    CREATE TEMPORARY TABLE {table}_tmp AS {query_str};
    CREATE EXTERNAL TABLE {table} LIKE {table}_tmp STORED AS PARQUET;
    ALTER TABLE {table} SET LOCATION '{url}';

    INSERT OVERWRITE TABLE {table}
        SELECT
            {columnar_query}
        FROM {table}_tmp;
    DROP TABLE {table};
"""

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
