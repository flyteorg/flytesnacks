import contextlib
import os
import sqlite3
import pandas
from flytekit import kwtypes, task, workflow
from flytekitplugins.sqlalchemy import SQLAlchemyConfig, SQLAlchemyTask


def sql_server() -> str:
    os.makedirs("sqlite3db", exist_ok=True)
    db_path = os.path.join("sqlite3db", "tracks.db")
    with contextlib.closing(sqlite3.connect(db_path)) as con:
        con.execute("create table tracks (TrackId bigint, Name text)")
        con.execute(
            "insert into tracks values (0, 'Sue'), (1, 'L'), (2, 'M'), (3, 'Ji'), (4, 'Po')"
        )
        con.commit()
    return f"sqlite:///{db_path}"


@task
def get_length(df: pandas.DataFrame) -> int:
    return len(df)


sql_task = SQLAlchemyTask(
    "sqlite_task",
    query_template="select * from tracks limit {{.inputs.limit}}",
    inputs=kwtypes(limit=int),
    task_config=SQLAlchemyConfig(uri="sqlite:///sqlite3db/tracks.db"),
)


@workflow
def my_wf(limit: int) -> int:
    return get_length(df=sql_task(limit=limit))


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Starting SqlServer at {sql_server()}")
    print(my_wf(limit=3))
