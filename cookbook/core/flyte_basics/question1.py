import typing

from flytekit import task, workflow, current_context
from flytekit.types.file import PNGImageFile


@task
def t1_simple(a: typing.Union[int, str]) -> str:
    if isinstance(a, int):
        return f"I'm an integer: {a}"
    else:
        return f"I'm a string: {a}"


@task
def t2_complex(b: PNGImageFile):
    current_context().default_deck.append(f'<img src="{b.remote_source}">')


@workflow
def demo_wf(a: typing.Union[int, str], b: PNGImageFile) -> str:
    r = t1_simple(a=a)
    t2_complex(b=b)

    return r
