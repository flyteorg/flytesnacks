from flytekit import current_context, task, workflow
from flytekit.exceptions.user import FlyteRecoverableException

RETRIES = 3


# Define a task to iterate precisely `n_iterations`, checkpoint its state, and recover from simulated failures.
@task(retries=RETRIES)
def use_checkpoint(n_iterations: int) -> int:
    cp = current_context().checkpoint
    prev = cp.read()

    start = 0
    if prev:
        start = int(prev.decode())

    # Create a failure interval to simulate failures across 'n' iterations and then succeed after configured retries
    failure_interval = n_iterations // RETRIES
    index = 0
    for index in range(start, n_iterations):
        # Simulate a deterministic failure for demonstration. Showcasing how it eventually completes within the given retries
        if index > start and index % failure_interval == 0:
            raise FlyteRecoverableException(f"Failed at iteration {index}, failure_interval {failure_interval}.")
        # Save progress state. It is also entirely possible to save state every few intervals
        cp.write(f"{index + 1}".encode())
    return index


# Create a workflow that invokes the task.
# The task will automatically undergo retries in the event of a FlyteRecoverableException.
@workflow
def checkpointing_example(n_iterations: int) -> int:
    return use_checkpoint(n_iterations=n_iterations)


# The local checkpoint is not utilized here because retries are not supported.
if __name__ == "__main__":
    try:
        checkpointing_example(n_iterations=10)
    except RuntimeError as e:  # noqa : F841
        # Since no retries are performed, an exception is expected when run locally
        pass
