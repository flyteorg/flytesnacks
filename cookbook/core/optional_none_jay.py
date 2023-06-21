from __future__ import absolute_import, division, print_function
from typing import Optional

from flytekit import task, workflow, dynamic
from flytekit.types.file import FlyteFile

@task
def hello(myfile: Optional[FlyteFile]) -> Optional[FlyteFile]:
    return None

@dynamic
def dyn_hello(myfile: Optional[FlyteFile]) -> Optional[FlyteFile]:
    return hello(myfile=myfile)


@workflow
def child_workflow(myfile: Optional[FlyteFile]) -> Optional[FlyteFile]:
    hello_output = dyn_hello(myfile=myfile)
    return hello_output
