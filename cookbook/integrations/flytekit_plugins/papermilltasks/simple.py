"""
Jupyter Notebook Task
---------------------

In this example, we will see how to create a flyte task that runs a simple notebook that accepts one input variable, transforms it and produces
an output. This example can be generalized to multiple inputs and outputs.
"""

# %%
# Import the necessary dependencies.
import math
import os
import pathlib
import flytekit
flytekit.current_context().execution_id.project
from flytekit import kwtypes, task, workflow
from flytekitplugins.papermill import NotebookTask

# %%
# Specifying inputs and outputs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# 1. After you are satisfied with the notebook, ensure that the first cell only has the input variables for the notebook. Add the tag ``parameters`` to the first cell.
#
#   .. image:: https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/parameters.png
#
# 2. Add ``outputs`` to the cell that returns the outputs.
#
# .. image:: https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/outputs.png
#
# 3. In a Python file, create a new ``NotebookTask`` at the module level.
nb = NotebookTask(
    name="simple-nb",
    notebook_path=os.path.join(
        pathlib.Path(__file__).parent.absolute(), "nb-simple.ipynb"
    ),
    render_deck=True,
    inputs=kwtypes(v=float),
    outputs=kwtypes(square=float),
)
#%%
# .. note::
#
#  - The ``notebook_path`` needs to be the absolute path to the actual notebook.
#  - The ``inputs`` and ``outputs`` variables need to match the variable names in the Jupyter notebook.
#  - You can see the notebook on Flyte deck if ``render_deck`` is set to ``True``.

# %%
# .. figure:: https://i.imgur.com/ogfVpr2.png
#   :alt: Notebook
#   :class: with-shadow
#
# Next declare a task that accepts the squared value from the notebook and provides a square root.
@task
def square_root_task(f: float) -> float:
    return math.sqrt(f)


# %%
# Treat the notebook task as a regular task and call it from within a flyte workflow.
@workflow
def nb_to_python_wf(f: float) -> float:
    out = nb(v=f)
    return square_root_task(f=out.square)


# %%
# You can run the task locally.
if __name__ == "__main__":
    print(nb_to_python_wf(f=3.14))

# %%
# Why are there 3 outputs?
# ^^^^^^^^^^^^^^^^^^^^^^^^
# On executing, you should see 3 outputs instead of the expected one, because this task generates 2 implicit outputs.
#
# One of them is the executed notebook (captured) and the other is a rendered (HTML) version of the executed notebook,
# which are named ``nb-simple-out.ipynb`` and ``nb-simple-out.html``, respectively.
