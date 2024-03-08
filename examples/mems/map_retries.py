import os
from collections import defaultdict
from flytekit import task, workflow
from flytekit.experimental import map_task


NUM_ATTEMPTS = defaultdict(int)


@task(retries=1)
def flakey_map_task(*, task_id: int) -> None:
    print(f"Envs {os.environ}")
    NUM_ATTEMPTS[task_id] += 1
    if NUM_ATTEMPTS[task_id] == 1:
        raise ValueError("Bad luck, this one failed")


@workflow
def flakey_map_workflow() -> None:
    task_ids = list(range(2))
    map_task(flakey_map_task)(task_id=task_ids)

