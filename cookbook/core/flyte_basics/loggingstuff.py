import logging

from flytekit import task, workflow

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(f"Settings at beginning of config: {logging.root.__dict__}")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
print(f"Settings at end of config: {logging.root.__dict__}")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


@task
def logger_task(value: int) -> int:
    print(f"Settings at task run start: {logging.root.__dict__}")
    logging.info("This is info")
    print(logging.root.__dict__)
    logging.warning(logging.root.__dict__)
    return value


@workflow
def logger_workflow(input_integer: int) -> int:
    return logger_task(value=input_integer)
