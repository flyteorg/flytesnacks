# %% [markdown]
# (airflow_agent_example_usage)=
# # Airflow agent example usage
# [Apache Airflow](https://airflow.apache.org) is a widely used open source
# platform for managing workflows with a robust ecosystem. Flyte provides an
# Airflow plugin that allows you to run Airflow tasks as Flyte tasks.
# This allows you to use the Airflow plugin ecosystem in conjunction with
# Flyte's powerful task execution and orchestration capabilities.
# %%

from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from flytekit import task, workflow


@task()
def t1():
    print("success")


# %% [markdown]
# Use the Airflow `FileSensor` to wait for a file to appear before running the task.
# %%
@workflow
def file_sensor():
    sensor = FileSensor(task_id="id", filepath="/tmp/1234")
    sensor >> t1()


# %% [markdown]
# Use the Airflow `BashOperator` to run a bash command.
# %%
@workflow
def bash_sensor():
    op = BashOperator(task_id="airflow_bash_operator", bash_command="echo hello")
    op >> t1()
