import logging
import multiprocessing as mp
import uuid
from typing import Optional, List

from flytekit import map_task, workflow, task, Resources
from flytekit.core.data_persistence import FileAccessProvider
from flytekit.loggers import logger
from flytekit.remote import FlyteRemote

logger.setLevel(logging.INFO)

FLYTE_HOST = "development.uniondemo.run"
DOMAIN = "development"
WORKFLOW_ID_TO_RUN = "core.control_flow.high_cpu_wf.single_integer_map_task"
WORKFLOW_VERSION_TO_RUN = "v4"


# Number of processes used to start workflows with
_NUMBER_OF_PROCESSES_TO_START_WORKFLOWS_WITH = 10
_NUMBER_OF_WORKFLOWS_TO_START = 250
_NUMBER_OF_TASKS_PER_WORKFLOW = 150


@task(requests=Resources(cpu="1", mem="1Gi"), limits=Resources(cpu="1", mem="1Gi"))
def single_integer_dummy_task(some_integer: int) -> int:
    return some_integer


@task(requests=Resources(cpu="1", mem="1Gi"), limits=Resources(cpu="1", mem="1Gi"))
def create_input_integers_task(number_of_inputs: int) -> List[int]:
    return list(range(number_of_inputs))


@workflow
def single_integer_map_task(number_of_inputs: int) -> None:
    input_integers = create_input_integers_task(number_of_inputs=number_of_inputs)
    map_task(single_integer_dummy_task)(some_integer=input_integers)


def start_workflow(random_id: str, input_integers_queue: mp.Queue) -> None:  # type: ignore
    remote = FlyteRemote.from_config(default_project="flytesnacks",
    default_domain="development",
    config_file_path="/Users/ketanumare/.flyte/config")
    flyte_workflow = remote.fetch_workflow(
        name=WORKFLOW_ID_TO_RUN,
        version=WORKFLOW_VERSION_TO_RUN,
    )
    while True:
        start_value: Optional[int] = input_integers_queue.get()
        if start_value is None:
            return
        remote.execute(
            flyte_workflow,
            inputs={"number_of_inputs": _NUMBER_OF_TASKS_PER_WORKFLOW},
            execution_name=f"scale-out-{random_id}-{start_value}",
        )
        print(f"Started workflow with id {start_value}")


def main() -> None:
    random_id = str(uuid.uuid4())[:4]
    print(f"Random id: {random_id}")
    input_queue = mp.Queue()  # type: ignore
    started_workers = []
    for _ in range(_NUMBER_OF_PROCESSES_TO_START_WORKFLOWS_WITH):
        worker = mp.Process(target=start_workflow, kwargs=dict(random_id=random_id, input_integers_queue=input_queue))
        worker.start()
        started_workers.append(worker)
    for i in range(_NUMBER_OF_WORKFLOWS_TO_START):
        input_queue.put(i)
    for _ in range(_NUMBER_OF_PROCESSES_TO_START_WORKFLOWS_WITH):
        input_queue.put(None)
    for worker in started_workers:
        worker.join()
    print(f"All workflows started with random id {random_id}")


if __name__ == "__main__":
    main()
