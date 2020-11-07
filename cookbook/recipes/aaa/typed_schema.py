import pandas
from flytekit.annotated.task import task, kwtypes
from flytekit.annotated.type_engine import FlyteSchema
from flytekit.annotated.workflow import workflow

out_schema = FlyteSchema[kwtypes(x=int, y=str)]


@task
def t1() -> out_schema:
    w = out_schema()
    df = pandas.DataFrame(data={"x": [1, 2], "y": ["3", "4"]})
    w.open().write(df)
    return w


@task
def t2(schema: FlyteSchema[kwtypes(x=int, y=str)]) -> FlyteSchema[kwtypes(x=int)]:
    assert isinstance(schema, FlyteSchema)
    df: pandas.DataFrame = schema.open().all()
    return df[schema.column_names()[:-1]]


@workflow
def wf() -> FlyteSchema[kwtypes(x=int)]:
    return t2(schema=t1())


if __name__ == "__main__":
    print(wf())
