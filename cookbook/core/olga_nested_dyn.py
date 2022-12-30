import typing
from datetime import datetime
from random import random, seed
from typing import Tuple

from flytekit import dynamic, task, workflow



@task
def t1(a: str):
    print(f"A is {a}")


@dynamic
def child(text: str):
    if len(text) > 10:
        t1(a=f"padded text...... {text}")
        t1(a=f"more padded text...... {text}")
        t1(a=f"lorem ipsum==========...... {text}")
    else:
        t1(a=f"Hello world 1 {text}")
        t1(a=f"Hello world 2 {text}")
        t1(a=f"Hello world 3 {text}")


@dynamic
def parent(text: str):
    words = text.split(" ")
    for w in words:
        child(text=w)


@workflow
def call_nested_dyn(text: str):
    parent(text=text)
