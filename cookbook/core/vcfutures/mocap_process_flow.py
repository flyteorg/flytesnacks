from algopipelines.flytedatapipeline.kubes import (
    mocap_expression_process,
    upload_folder,
)

from algopipelines.datahandler.k8s import task_config
from flytekit import dynamic
from flytekit.types.directory import FlyteDirectory


@dynamic(**task_config(
    image='algopipelines-generic:v1',
    cpu='400m', memory='400Mi'))
def mocap_process_flow(dummy: bool):

    expression_process_outputs = mocap_expression_process(dummy=dummy)
    upload_folder(dummy=dummy)

