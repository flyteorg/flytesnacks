import logging

from flytekit import ContainerTask, ImageSpec, kwtypes, task, workflow
from flytekit.core.base_task import TaskMetadata

logger = logging.getLogger(__file__)

# A `flytekit.ContainerTask` denotes an arbitrary container. In the following example, the name of the task
# is `calculate_ellipse_area_shell`. This name has to be unique in the entire project. Users can specify:
#
# - `input_data_dir` -> where inputs will be written to.
# - `output_data_dir` -> where Flyte will expect the outputs to exist.

# `inputs` and `outputs` specify the interface for the task; thus it should be an ordered dictionary of typed input and
# output variables.
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
    metadata=TaskMetadata(cache=True, cache_version="1.0"),
)

# use `ImageSpec` to copy files or directories into container `/root`
calculate_ellipse_area_python = ContainerTask(
    name="ellipse-area-metadata-python",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float, metadata=str),
    image=ImageSpec(
        base_image="ghcr.io/flyteorg/rawcontainers-python:v2",
        registry="localhost:30000",
        builder="default",
        copy=["calculate-ellipse-area-new.py"],
    ),
    command=[
        "python",
        "calculate-ellipse-area-new.py",
        "{{.inputs.a}}",
        "{{.inputs.b}}",
        "/var/outputs",
    ],
    metadata=TaskMetadata(cache=True, cache_version="1.0"),
)

calculate_ellipse_area_r = ContainerTask(
    name="ellipse-area-metadata-r",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float, metadata=str),
    image="ghcr.io/flyteorg/rawcontainers-r:v2",
    command=[
        "Rscript",
        "--vanilla",
        "calculate-ellipse-area.R",
        "{{.inputs.a}}",
        "{{.inputs.b}}",
        "/var/outputs",
    ],
    metadata=TaskMetadata(cache=True, cache_version="1.0"),
)

calculate_ellipse_area_haskell = ContainerTask(
    name="ellipse-area-metadata-haskell",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float, metadata=str),
    image="ghcr.io/flyteorg/rawcontainers-haskell:v2",
    command=[
        "./calculate-ellipse-area",
        "{{.inputs.a}}",
        "{{.inputs.b}}",
        "/var/outputs",
    ],
    metadata=TaskMetadata(cache=True, cache_version="1.0"),
)

calculate_ellipse_area_julia = ContainerTask(
    name="ellipse-area-metadata-julia",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float, metadata=str),
    image="ghcr.io/flyteorg/rawcontainers-julia:v2",
    command=[
        "julia",
        "calculate-ellipse-area.jl",
        "{{.inputs.a}}",
        "{{.inputs.b}}",
        "/var/outputs",
    ],
    metadata=TaskMetadata(cache=True, cache_version="1.0"),
)


@task
def report_all_calculated_areas(
    area_shell: float,
    metadata_shell: str,
    area_python: float,
    metadata_python: str,
    area_r: float,
    metadata_r: str,
    area_haskell: float,
    metadata_haskell: str,
    area_julia: float,
    metadata_julia: str,
):
    logger.info(f"shell: area={area_shell}, metadata={metadata_shell}")
    logger.info(f"python: area={area_python}, metadata={metadata_python}")
    logger.info(f"r: area={area_r}, metadata={metadata_r}")
    logger.info(f"haskell: area={area_haskell}, metadata={metadata_haskell}")
    logger.info(f"julia: area={area_julia}, metadata={metadata_julia}")


# If you’re using Flytekit version >= v1.11.1, you can execute it locally.
# For example, `pyflyte run raw_container.py calculate_ellipse_area_shell --a 1.1 --b 1.2`
#
# As can be seen in this example, `ContainerTask`s can be interacted with like normal Python functions, whose inputs
# correspond to the declared input variables. All data returned by the tasks are consumed and logged by a Flyte task.
@workflow
def wf(a: float, b: float):
    # Calculate area in all languages
    area_shell, metadata_shell = calculate_ellipse_area_shell(a=a, b=b)
    area_python, metadata_python = calculate_ellipse_area_python(a=a, b=b)
    area_r, metadata_r = calculate_ellipse_area_r(a=a, b=b)
    area_haskell, metadata_haskell = calculate_ellipse_area_haskell(a=a, b=b)
    area_julia, metadata_julia = calculate_ellipse_area_julia(a=a, b=b)

    # Report on all results in a single task to simplify comparison
    report_all_calculated_areas(
        area_shell=area_shell,
        metadata_shell=metadata_shell,
        area_python=area_python,
        metadata_python=metadata_python,
        area_r=area_r,
        metadata_r=metadata_r,
        area_haskell=area_haskell,
        metadata_haskell=metadata_haskell,
        area_julia=area_julia,
        metadata_julia=metadata_julia,
    )
