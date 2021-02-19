import math
import os
import pathlib

from flytekit import kwtypes, task, workflow
from flytekitplugins.papermill import NotebookTask

nb = NotebookTask(
    name="simple-nb",
    notebook_path=os.path.join(pathlib.Path(__file__).parent.absolute(), "nb-simple.ipynb"),
    inputs=kwtypes(v=float),
    outputs=kwtypes(square=float),
)


@task
def square_root_task(f: float) -> float:
    return math.sqrt(f)


@workflow
def nb_to_python_wf(f: float) -> float:
    out = nb(v=f)
    return square_root_task(f=out.square)


if __name__ == "__main__":
    print(nb_to_python_wf(f=3.14))
