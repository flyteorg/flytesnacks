import datetime
import inspect
import typing

import flytekit.annotated.task
import flytekit.annotated.workflow
from flytekit.annotated import context_manager, promise
from flytekit.annotated.context_manager import FlyteContext, ExecutionState
from flytekit.annotated.task import task, AbstractSQLTask, metadata, maptask, dynamic
from flytekit.annotated.workflow import workflow
from flytekit.annotated.interface import extract_return_annotation, transform_variable_map


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"


@task
def t2(a: str, b: str) -> str:
    return b + a


@workflow
def my_wf(a: int, b: str) -> (int, str):
    x, y = t1(a=a)
    d = t2(a=y, b=b)
    return x, d
