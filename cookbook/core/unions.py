from typing import Optional

from flytekit import workflow, task


@task
def t1(my_opt: Optional[int]):
    if my_opt is None:
        print("none")
    else:
        print(f"not none value was {my_opt}")


@workflow
def wf_opt(my_opt: Optional[int] = None):
    return t1(my_opt=my_opt)


@workflow
def opt_parent():
    return wf_opt()
