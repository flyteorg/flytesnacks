import pandas
from flytekit import kwtypes, task, workflow
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task

# https://www.sqlitetutorial.net/sqlite-sample-database/
from flytekit.types.schema import FlyteSchema

EXAMPLE_DB = "https://cdn.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip"

sql_task = SQLite3Task(
    name="cookbook.sqlite3.sample",
    query_template="select TrackId, Name from tracks limit {{.inputs.limit}}",
    inputs=kwtypes(limit=int),
    output_schema_type=FlyteSchema[kwtypes(TrackId=int, Name=str)],
    task_config=SQLite3Config(uri=EXAMPLE_DB, compressed=True,),
)


@task
def print_and_count_columns(df: pandas.DataFrame) -> int:
    return len(df[df.columns[0]])


@workflow
def wf() -> int:
    return print_and_count_columns(df=sql_task(limit=100))
