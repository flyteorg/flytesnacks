from pathlib import Path
from typing import Tuple

import flytekit
from flytekit import kwtypes, task, workflow
from flytekit.extras.tasks.shell import OutputLocation, ShellTask
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile


t1 = ShellTask(
    name="task_1",
    debug=True,
    script="""
    set -ex
    echo "Hey there! Let's run some bash scripts using Flyte's ShellTask."
    echo "Showcasing Flyte's Shell Task." >> {inputs.x}
    if grep "Flyte" {inputs.x}
    then
        echo "Found it!" >> {inputs.x}
    else
        echo "Not found!"
    fi
    """,
    inputs=kwtypes(x=FlyteFile),
    output_locs=[OutputLocation(var="i", var_type=FlyteFile, location="{inputs.x}")],
)


t2 = ShellTask(
    name="task_2",
    debug=True,
    script="""
    set -ex
    cp {inputs.x} {inputs.y}
    tar -zcvf {outputs.j} {inputs.y}
    """,
    inputs=kwtypes(x=FlyteFile, y=FlyteDirectory),
    output_locs=[OutputLocation(var="j", var_type=FlyteFile, location="{inputs.y}.tar.gz")],
)


t3 = ShellTask(
    name="task_3",
    debug=True,
    script="""
    set -ex
    tar -zxvf {inputs.z}
    cat {inputs.y}/$(basename {inputs.x}) | wc -m > {outputs.k}
    """,
    inputs=kwtypes(x=FlyteFile, y=FlyteDirectory, z=FlyteFile),
    output_locs=[OutputLocation(var="k", var_type=FlyteFile, location="output.txt")],
)


@task
def create_entities() -> Tuple[FlyteFile, FlyteDirectory]:
    working_dir = Path(flytekit.current_context().working_directory)
    flytefile = working_dir / "test.txt"
    flytefile.touch()

    flytedir = working_dir / "testdata"
    flytedir.mkdir(exist_ok=True)

    flytedir_file = flytedir / ".gitkeep"
    flytedir_file.touch()
    return flytefile, flytedir


@workflow
def shell_task_wf() -> FlyteFile:
    x, y = create_entities()
    t1_out = t1(x=x)
    t2_out = t2(x=t1_out, y=y)
    t3_out = t3(x=x, y=y, z=t2_out)
    return t3_out


if __name__ == "__main__":
    print(f"Running shell_task_wf() {shell_task_wf()}")
