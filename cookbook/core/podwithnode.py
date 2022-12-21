import os
import time
from typing import List

from flytekit import Resources, TaskMetadata, dynamic, map_task, task, workflow
from flytekitplugins.pod import Pod
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1ResourceRequirements,
    V1Volume,
)

_SHARED_DATA_PATH = "/data/message.txt"


def generate_pod_spec_for_task():
    primary_container = V1Container(name="primary")

    pod_spec = V1PodSpec(
        containers=[primary_container],
    )
    return pod_spec


def generate_pod():
    p = Pod(
        pod_spec=V1PodSpec(
            containers=[
                V1Container(name="primary"),
            ],
            node_selector={"node_group": "memory"},
        ),
        primary_container_name="primary",
    )
    return p


@task(
    task_config=generate_pod(),
    requests=Resources(
        mem="1G",
    ),
)
def my_pod_task():
    print("hello world")
    time.sleep(30000)


@workflow
def pod_workflow():
    my_pod_task()


@task(
    task_config=generate_pod(),
    requests=Resources(
        mem="200Mi",
    ),
)
def my_pod_map_task(stringify: int) -> str:
    return str(stringify)


@workflow
def my_map_workflow(a: List[int]) -> List[str]:
    mapped_out = map_task(my_pod_map_task, metadata=TaskMetadata(retries=1))(
        stringify=a
    )
    return mapped_out


# @task(
#     task_config=Pod(
#         pod_spec=V1PodSpec(
#             containers=[
#                 V1Container(
#                     name="primary",
#                     resources=V1ResourceRequirements(
#                         requests={"cpu": ".5", "memory": "500Mi"},
#                         limits={"cpu": ".5", "memory": "500Mi"},
#                     ),
#                 )
#             ],
#             init_containers=[
#                 V1Container(
#                     image="alpine",
#                     name="init",
#                     command=["/bin/sh"],
#                     args=["-c", 'echo "I\'m a customizable init container"'],
#                     resources=V1ResourceRequirements(
#                         limits={"cpu": ".5", "memory": "500Mi"},
#                     ),
#                 )
#             ],
#         ),
#         primary_container_name="primary",
#     )
# )
# def my_pod_map_task(stringify: int) -> str:
#     return str(stringify)


# @workflow
# def my_map_workflow(a: List[int]) -> str:
#     mapped_out = map_task(my_pod_map_task, metadata=TaskMetadata(retries=1))(
#         stringify=a
#     )
#     coalesced = coalesce(b=mapped_out)
#     return coalesced


