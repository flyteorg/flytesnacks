from flyteidl.core.security_pb2 import Secret
from flytekit import workflow
from flytekit.types.schema import FlyteSchema
from flytekitplugins.snowflake import SnowflakeConfig, SnowflakeTask

tk = SnowflakeTask(
    "test_snowflake",
    query_template='select * from "DEMO_DB"."PUBLIC"."SAMPLE"',
    task_config=SnowflakeConfig(
        account_name='hoa61102',
        username="haytham",
        password=Secret(group="snowflake", key="password"),
        db="DEMO_DB",
        schema="PUBLIC",
        warehouse="COMPUTE_WH"
    ),
    output_schema_type=FlyteSchema,
)


@workflow
def snowflake_query() -> FlyteSchema:
    return tk()
