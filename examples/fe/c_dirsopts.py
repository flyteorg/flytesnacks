import typing

from flytekit.core.task import task
from flytekit.core.workflow import workflow
from flytekit.types.directory import FlyteDirectory


@task
def take_coll_opt_dirs(a: typing.List[typing.Optional[FlyteDirectory]]):
    for aa in a:
        if aa is None:
            print("got none")
        else:
            print(aa.remote_source)


@workflow
def wf_run_take_coll_opt_dirs(a: typing.List[typing.Optional[FlyteDirectory]]):
    take_coll_opt_dirs(a=a)

