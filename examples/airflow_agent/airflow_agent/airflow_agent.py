from airflow.sensors.filesystem import FileSensor
from flytekit import task, workflow


@task()
def t1():
    print("flyte")


@workflow
def wf():
    sensor = FileSensor(task_id="id", filepath="/tmp/1234")
    sensor >> t1()


if __name__ == "__main__":
    wf()
