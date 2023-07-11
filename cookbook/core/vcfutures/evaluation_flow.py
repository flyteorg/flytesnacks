from algopipelines.flytedatapipeline.evaluators_kubes import (
    evaluation,
    download_evaluation_inputs,
)

from algopipelines.datahandler.k8s import task_config
from algopipelines.flytedatapipeline.kubes import (
    upload_status_file,
    upload_folder,
)

from flytekit import dynamic


@dynamic(**task_config(
    image='algopipelines-generic:v1',
    cpu='400m', memory='400Mi'))
def evaluation_flow(dummy: bool, ):
    evaluation_inputs = download_evaluation_inputs(dummy=dummy)
    evaluation_output = evaluation(dummy=dummy)

    upload_status_file(dummy=dummy)
    upload_folder(dummy=dummy)
