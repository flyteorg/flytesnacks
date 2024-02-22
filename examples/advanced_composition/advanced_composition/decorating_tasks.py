import logging
from functools import partial, wraps

from flytekit import task, workflow

logger = logging.getLogger(__file__)


def log_io(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info(f"task {fn.__name__} called with args: {args}, kwargs: {kwargs}")
        out = fn(*args, **kwargs)
        logger.info(f"task {fn.__name__} output: {out}")
        return out

    return wrapper


@task
@log_io
def t1(x: int) -> int:
    return x + 1


def validate_output(fn=None, *, floor=0):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        out = fn(*args, **kwargs)
        if out <= floor:
            raise ValueError(f"output of task {fn.__name__} must be a positive number, found {out}")
        return out

    if fn is None:
        return partial(validate_output, floor=floor)

    return wrapper


@task
@log_io
@validate_output(floor=10)
def t2(x: int) -> int:
    return x + 10


@workflow
def decorating_task_wf(x: int) -> int:
    return t2(x=t1(x=x))


if __name__ == "__main__":
    print(f"Running decorating_task_wf(x=10) {decorating_task_wf(x=10)}")
