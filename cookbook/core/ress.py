import logging

from flytekit import ContainerTask, kwtypes, task, workflow
from flytekit.core.pod_template import PodTemplate
from kubernetes.client.models import V1PodSpec, V1Toleration

logger = logging.getLogger(__file__)


# effect=None, key=None, operator=None, toleration_seconds=None, value=None, local_vars_configuration=None)
ps = V1PodSpec(containers=[], tolerations=[V1Toleration(effect="NoSchedule", key="num-gpus", operator="Equal", value="1")])
pt = PodTemplate(pod_spec=ps, labels={"somelabel": "ilovepizza"})


calculate_ellipse_area_shell = ContainerTask(
    name="ellipse-area-metadata-shell",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float, metadata=str),
    image="ghcr.io/flyteorg/rawcontainers-shell:v2",
    command=[
        "./calculate-ellipse-area.sh",
        "{{.inputs.a}}",
        "{{.inputs.b}}",
        "/var/outputs",
    ],
    pod_template=pt,
)
