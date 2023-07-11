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

    def add_attribute(self,
                      name: str,
                      value: FlyteFile):
        attribute = Inner(name=name, value=value)
        self.inner_dict[name] = attribute


@dataclass_json
@dataclass
class Parent:
    outer: Outer


@task
def t1(a: Outer) -> Outer:
    print(f"This is a: {a=}")
    a.add_attribute(name="more", value=FlyteFile("/Users/ytong/temp/data/source/more.txt"))
    return a


@task
def t2(a: Outer) -> Parent:
    print(f"t2 this is a: {a=}")
    if len(a.inner) > 0:
        with open(a.inner[0].value, "r") as f:
            print(f.read())
    else:
        for k in a.inner_dict.keys():
            print(f"Found key {k}")
            with open(a.inner_dict[k].value, "r") as f:
                print(f.read())

    return Parent(outer=a)


@task
def t3(a: Parent):
    print(f"t2 this is a: {a=}")
    if len(a.outer.inner) > 0:
        with open(a.outer.inner[0].value, "r") as f:
            print(f.read())
    else:
        for k in a.outer.inner_dict.keys():
            print(f"Found key {k}")
            with open(a.outer.inner_dict[k].value, "r") as f:
                print(f.read())


@workflow
def wf(a: Outer):
    aa = t1(a=a)
    p = t2(a=aa)
    t3(a=p)


if __name__ == "__main__":
    # o = Outer(name="outer", inner=[Inner(name="inner", value=FlyteFile("/Users/ytong/temp/data/source/original.txt"))])
    # wf(a=o)

    o2 = Outer(name="outer", inner=[], inner_dict={"aaa": Inner(name="inner", value=FlyteFile(
        "/Users/ytong/temp/data/source/original.txt"))})
    wf(a=o2)
