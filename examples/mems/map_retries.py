import os
from random import randint
from collections import defaultdict
from flytekit import task, workflow
from flytekit.experimental import map_task
from flytekit.exceptions.base import FlyteRecoverableException

NUM_ATTEMPTS = defaultdict(int)


@task(retries=2)
def flakey_map_task(*, task_id: int) -> None:
    attempt = os.environ["FLYTE_ATTEMPT_NUMBER"]
    print(f"Task attempt: {attempt}")

    r = randint(0, 10)
    print(f"Random number is: {r}")
    if r < 5:
        print("Failing task")
        raise FlyteRecoverableException(f"Bad luck, this one failed {task_id}")


@workflow
def flakey_map_workflow() -> None:
    task_ids = list(range(3))
    map_task(flakey_map_task)(task_id=task_ids)
