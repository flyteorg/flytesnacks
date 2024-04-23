from flytekit import kwtypes, workflow
from flytekitplugins.snowflake import SnowflakeConfig, SnowflakeTask


snowflake_task_no_io = SnowflakeTask(
    name="sql.snowflake.no_io",
    inputs={},
    query_template="SELECT 1",
    output_schema_type=None,
    task_config=SnowflakeConfig(
        account="<SNOWFLAKE_ACCOUNT_ID>",
        database="SNOWFLAKE_SAMPLE_DATA",
        schema="TPCH_SF1000",
        warehouse="COMPUTE_WH",
    ),
)


snowflake_task_templatized_query = SnowflakeTask(
    name="sql.snowflake.w_io",
    # Define inputs as well as their types that can be used to customize the query.
    inputs=kwtypes(nation_key=int),
    task_config=SnowflakeConfig(
        account="<SNOWFLAKE_ACCOUNT_ID>",
        database="SNOWFLAKE_SAMPLE_DATA",
        schema="TPCH_SF1000",
        warehouse="COMPUTE_WH",
    ),
    query_template="SELECT * from CUSTOMER where C_NATIONKEY =  {{ .inputs.nation_key }} limit 100",
)


@workflow
def snowflake_wf(nation_key: int):
    return snowflake_task_templatized_query(nation_key=nation_key)


# To review the query results, access the Snowflake console at:
# `https://<SNOWFLAKE_ACCOUNT_ID>.snowflakecomputing.com/console#/monitoring/queries/detail`.
#
# You can also execute the task and workflow locally.
if __name__ == "__main__":
    print(snowflake_task_no_io())
    print(snowflake_wf(nation_key=10))
