import os
from random import randint
from collections import defaultdict
from flytekit import task, workflow
from flytekit.experimental import map_task


NUM_ATTEMPTS = defaultdict(int)


@task(retries=2)
def flakey_map_task(*, task_id: int) -> None:
    for x, y in os.environ.items():
        print(f"{x}: {y}")

    r = randint(0, 10)
    print(f"Random number: {r}")
    if r < 5:
        print("Failing")
        raise ValueError("Bad luck, this one failed")


@workflow
def flakey_map_workflow() -> None:
    task_ids = list(range(3))
    map_task(flakey_map_task)(task_id=task_ids)

