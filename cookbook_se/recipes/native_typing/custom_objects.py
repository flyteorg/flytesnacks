"""
This examples shows how users can serialize custom JSON'able dataclasses between successive tasks using the excellent
@dataclasses_json library
"""
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from flytekit import task, workflow


@dataclass_json
@dataclass
class Datum(object):
    x: int
    y: str
    z: typing.Dict[int, str]


@task
def stringify(x: int) -> Datum:
    return Datum(x=x, y=str(x), z={x: str(x)})


@task
def add(x: Datum, y: Datum) -> Datum:
    x.z.update(y.z)
    return Datum(x=x.x + y.x, y=x.y + y.y, z=x.z)


@workflow
def wf(x: int, y: int) -> Datum:
    return add(x=stringify(x=x), y=stringify(x=y))


if __name__ == "__main__":
    wf(x=10, y=20)

