from flytekit import workflow
from flytekit.types.schema import FlyteSchema
from flytekitplugins.snowflake import SnowflakeConfig, SnowflakeTask

tk = SnowflakeTask(
    "test_snowflake",
    query_template='select * from "DEMO_DB"."PUBLIC"."SAMPLE"',
    task_config=SnowflakeConfig(
        uri='snowflake://{user}:{password}@{account}/'.format(
            user='haytham',
            password='<your_password>',
            account='hoa61102',
        ),
        # secret_connect_args={
        #     "password": Secret(group="snowflake", key="password"),
        # }
        # username="haytham",
        # password=Secret(group="snowflake", key="password"),
        # db="DEMO_DB",
        # schema="PUBLIC",
        # warehouse="COMPUTE_WH"
    ),
    output_schema_type=FlyteSchema,
)


@workflow
def snowflake_query() -> FlyteSchema:
    return tk()
