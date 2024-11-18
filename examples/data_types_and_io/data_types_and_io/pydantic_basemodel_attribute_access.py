from typing import Dict, List
from flytekit.types.file import FlyteFile
from flytekit import task, workflow, ImageSpec
from enum import Enum
from pydantic import BaseModel, Field

image_spec = ImageSpec(
    registry="ghcr.io/flyteorg",
    packages=["pydantic"],
)

class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class InnerBM(BaseModel):
    a: int = -1
    b: float = 2.1
    c: str = "Hello, Flyte"
    d: bool = False
    e: List[int] = Field(default_factory=lambda: [0, 1, 2, -1, -2])
    f: List[FlyteFile] = Field(default_factory=lambda: [
        FlyteFile(
            "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
        )
    ])
    g: List[List[int]] = Field(default_factory=lambda: [[0], [1], [-1]])
    h: List[Dict[int, bool]] = Field(default_factory=lambda: [{0: False}, {1: True}, {-1: True}])
    i: Dict[int, bool] = Field(default_factory=lambda: {0: False, 1: True, -1: False})
    j: Dict[int, FlyteFile] = Field(
        default_factory=lambda: {
            0: FlyteFile(
                "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
            ),
            1: FlyteFile(
                "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
            ),
            -1: FlyteFile(
                "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
            ),
        }
    )
    k: Dict[int, List[int]] = Field(default_factory=lambda: {0: [0, 1, -1]})
    l: Dict[int, Dict[int, int]] = Field(default_factory=lambda: {1: {-1: 0}})
    m: dict = Field(default_factory=lambda: {"key": "value"})
    n: FlyteFile = Field(
        default_factory=lambda: FlyteFile(
            "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
        )
    )
    enum_status: Status = Status.PENDING


class BM(BaseModel):
    a: int = -1
    b: float = 2.1
    c: str = "Hello, Flyte"
    d: bool = False
    e: List[int] = Field(default_factory=lambda: [0, 1, 2, -1, -2])
    f: List[FlyteFile] = Field(default_factory=lambda: [
        FlyteFile(
            "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
        )
    ])
    g: List[List[int]] = Field(default_factory=lambda: [[0], [1], [-1]])
    h: List[Dict[int, bool]] = Field(default_factory=lambda: [{0: False}, {1: True}, {-1: True}])
    i: Dict[int, bool] = Field(default_factory=lambda: {0: False, 1: True, -1: False})
    j: Dict[int, FlyteFile] = Field(
        default_factory=lambda: {
            0: FlyteFile(
                "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
            ),
            1: FlyteFile(
                "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
            ),
            -1: FlyteFile(
                "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
            ),
        }
    )
    k: Dict[int, List[int]] = Field(default_factory=lambda: {0: [0, 1, -1]})
    l: Dict[int, Dict[int, int]] = Field(default_factory=lambda: {1: {-1: 0}})
    m: dict = Field(default_factory=lambda: {"key": "value"})
    n: FlyteFile = Field(
        default_factory=lambda: FlyteFile(
            "https://raw.githubusercontent.com/flyteorg/flytesnacks/refs/heads/master/examples/data_types_and_io/data_types_and_io/attribute_access.py"
        )
    )
    inner_bm: InnerBM = Field(default_factory=InnerBM)
    enum_status: Status = Status.PENDING


@task(container_image=image)
def t_bm(bm: BM) -> BM:
    return bm


@task(container_image=image)
def t_inner(inner_bm: InnerBM) -> InnerBM:
    assert isinstance(inner_bm, InnerBM), "inner_bm is not of type InnerBM"

    # f: List[FlyteFile]
    for ff in inner_bm.f:
        assert isinstance(ff, FlyteFile), "Expected FlyteFile"
        with open(ff, "r") as f:
            print(f.read())

    # j: Dict[int, FlyteFile]
    for _, ff in inner_bm.j.items():
        assert isinstance(ff, FlyteFile), "Expected FlyteFile in j"
        with open(ff, "r") as f:
            print(f.read())

    # n: FlyteFile
    assert isinstance(inner_bm.n, FlyteFile), "n is not FlyteFile"
    with open(inner_bm.n, "r") as f:
        print(f.read())

    assert inner_bm.enum_status == Status.PENDING, "enum_status does not match"

    return inner_bm


@task(container_image=image)
def t_test_all_attributes(
    a: int,
    b: float,
    c: str,
    d: bool,
    e: List[int],
    f: List[FlyteFile],
    g: List[List[int]],
    h: List[Dict[int, bool]],
    i: Dict[int, bool],
    j: Dict[int, FlyteFile],
    k: Dict[int, List[int]],
    l: Dict[int, Dict[int, int]],
    m: dict,
    n: FlyteFile,
    enum_status: Status,
):

    # Strict type checks for simple types
    assert isinstance(a, int), f"a is not int, it's {type(a)}"
    assert a == -1
    assert isinstance(b, float), f"b is not float, it's {type(b)}"
    assert isinstance(c, str), f"c is not str, it's {type(c)}"
    assert isinstance(d, bool), f"d is not bool, it's {type(d)}"

    # Strict type checks for List[int]
    assert isinstance(e, list) and all(isinstance(i, int) for i in e), "e is not List[int]"

    # Strict type checks for List[FlyteFile]
    assert isinstance(f, list) and all(isinstance(i, FlyteFile) for i in f), "f is not List[FlyteFile]"

    # Strict type checks for List[List[int]]
    assert isinstance(g, list) and all(
        isinstance(i, list) and all(isinstance(j, int) for j in i) for i in g
    ), "g is not List[List[int]]"

    # Strict type checks for List[Dict[int, bool]]
    assert isinstance(h, list) and all(
        isinstance(i, dict) and all(isinstance(k, int) and isinstance(v, bool) for k, v in i.items()) for i in h
    ), "h is not List[Dict[int, bool]]"

    # Strict type checks for Dict[int, bool]
    assert isinstance(i, dict) and all(
        isinstance(k, int) and isinstance(v, bool) for k, v in i.items()
    ), "i is not Dict[int, bool]"

    # Strict type checks for Dict[int, FlyteFile]
    assert isinstance(j, dict) and all(
        isinstance(k, int) and isinstance(v, FlyteFile) for k, v in j.items()
    ), "j is not Dict[int, FlyteFile]"

    # Strict type checks for Dict[int, List[int]]
    assert isinstance(k, dict) and all(
        isinstance(k, int) and isinstance(v, list) and all(isinstance(i, int) for i in v) for k, v in k.items()
    ), "k is not Dict[int, List[int]]"

    # Strict type checks for Dict[int, Dict[int, int]]
    assert isinstance(l, dict) and all(
        isinstance(k, int) and isinstance(v, dict) and all(isinstance(sub_k, int) and isinstance(sub_v, int) for sub_k, sub_v in v.items())
        for k, v in l.items()
    ), "l is not Dict[int, Dict[int, int]]"

    # Strict type check for a generic dict
    assert isinstance(m, dict), "m is not dict"

    # Strict type check for FlyteFile
    assert isinstance(n, FlyteFile), "n is not FlyteFile"

    # Strict type check for Enum
    assert isinstance(enum_status, Status), "enum_status is not Status"

    print("All attributes passed strict type checks.")


@workflow
def wf(bm: BM):
    new_bm = t_bm(bm=bm)
    t_inner(new_bm.inner_bm)
    t_test_all_attributes(
        a=new_bm.a,
        b=new_bm.b,
        c=new_bm.c,
        d=new_bm.d,
        e=new_bm.e,
        f=new_bm.f,
        g=new_bm.g,
        h=new_bm.h,
        i=new_bm.i,
        j=new_bm.j,
        k=new_bm.k,
        l=new_bm.l,
        m=new_bm.m,
        n=new_bm.n,
        enum_status=new_bm.enum_status,
    )
    t_test_all_attributes(
        a=new_bm.inner_bm.a,
        b=new_bm.inner_bm.b,
        c=new_bm.inner_bm.c,
        d=new_bm.inner_bm.d,
        e=new_bm.inner_bm.e,
        f=new_bm.inner_bm.f,
        g=new_bm.inner_bm.g,
        h=new_bm.inner_bm.h,
        i=new_bm.inner_bm.i,
        j=new_bm.inner_bm.j,
        k=new_bm.inner_bm.k,
        l=new_bm.inner_bm.l,
        m=new_bm.inner_bm.m,
        n=new_bm.inner_bm.n,
        enum_status=new_bm.inner_bm.enum_status,
    )
