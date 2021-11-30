from flytekit import task, workflow
from flytekit import ContainerTask, kwtypes, workflow


calculate_ellipse_area = ContainerTask(
    name="ellipse-area-bash",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float),
    image="alpine",
    command=[
        'sh',
        '-c',
        'echo "4*a(1) * {{ .Inputs.a }} * {{ .Inputs.b }}" | bc -l | tee /var/outputs/area',
    ],
)

@workflow
def wf(a: float, b: float) -> float:
    return calculate_ellipse_area(a=a, b=b)
