"""
Using custom objects
-------------------------

Flyte supports passing JSON's between tasks. But, to simplify the usage for the users and introduce type-safety,
flytekit supports passing custom data objects between tasks. Currently only dataclasses that are decorated with
@dataclasses_json are supported.

This example shows how users can serialize custom JSON'able dataclasses between successive tasks using the excellent
`dataclasses_json <https://pypi.org/project/dataclasses-json/>` library
"""
from flytekit import task, workflow
import typing
from enum import Enum


# %%
# Enums are natively supported in flyte's type system. Enum values can only be of type string. At runtime they are
# represented using their string values.
#
# .. note::
#
#   ENUM Values can only be string. Other languages will receive enum as a string.
#
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


# %%
# Enums can be used as a regular type
@task
def enum_stringify(c: Color) -> str:
    return c.value


# %%
# Their values can be accepted as string
@task
def string_to_enum(c: str) -> Color:
    return Color(c)


@workflow
def enum_wf(c: Color = Color.RED) -> (Color, str):
    v = enum_stringify(c=c)
    return string_to_enum(c=v), v


if __name__ == "__main__":
    print(enum_wf())
