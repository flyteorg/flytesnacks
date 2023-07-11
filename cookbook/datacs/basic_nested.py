from dataclasses_json import dataclass_json
from dataclasses import dataclass, field

from flytekit import task, workflow
from flytekit.types.file import FlyteFile


@dataclass_json
@dataclass
class Inner:
    name: str
    value: FlyteFile


@dataclass_json
@dataclass
class Outer:
    name: str
    inner: Inner


@task
def t1(a: Outer) -> Outer:
    print(f"This is a: {a=}")
    return a


@task
def t2(a: Outer):
    print(f"t2 this is a: {a=}")
    with open(a.inner.value, "r") as f:
        print(f.read())


@workflow
def wf(a: Outer):
    aa = t1(a=a)
    t2(a=aa)


if __name__ == "__main__":
    o = Outer(name="outer", inner=Inner(name="inner", value=FlyteFile("/Users/ytong/temp/data/source/original.txt")))
    wf(a=o)
