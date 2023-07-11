import typing
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
    inner: typing.List[Inner]
    inner_dict: typing.Dict[str, Inner] = field(default_factory=dict)


@task
def t1(a: Outer) -> Outer:
    print(f"This is a: {a=}")
    return a


@task
def t2(a: Outer):
    print(f"t2 this is a: {a=}")
    if len(a.inner) > 0:
        with open(a.inner[0].value, "r") as f:
            print(f.read())
    else:
        with open(a.inner_dict["aaa"].value, "r") as f:
            print(f.read())


@workflow
def wf(a: Outer):
    aa = t1(a=a)
    t2(a=aa)


if __name__ == "__main__":
    o = Outer(name="outer", inner=[Inner(name="inner", value=FlyteFile("/Users/ytong/temp/data/source/original.txt"))])
    wf(a=o)

    o2 = Outer(name="outer", inner=[], inner_dict={"aaa": Inner(name="inner", value=FlyteFile(
        "/Users/ytong/temp/data/source/original.txt"))})
    wf(a=o2)
