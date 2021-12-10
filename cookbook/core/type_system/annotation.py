"""
.. _annotations:

Parameter Annotations
--------------------------

This example explains how to annotate parameters within Flyte. These
annotations are supposed to be semantic descriptions of types and are
accessible from the serialized flyteidl LiteralType message. They arenot
accesible at runtime within a task.

"""
import typing

from flytekit import task, workflow

# %%
# Flytekit has an object to hold annotations.
from flytekit.core.annotation import FlyteAnnotation

# %%
# FlyteAnnotation can hold arbitrary data objects and should be stuffed inside
# the `typing.Annotated` type guard.
typing.Annotated[int, FlyteAnnotation({"some": "data"})]

# %%
# To use annotations, import the `flytekit.core.annotation.FlyteAnnotation`
# object and use it within typing.Annotation guards like so:


@task
def t1(a: typing.Annotated[int, FlyteAnnotation({"foo": {"bar": 1}})], b: str) -> str:
    return f"{a} b"


@workflow
def wf() -> int:
    return t1(1, "fizz")


if __name__ == "__main__":
    print(wf())
