from __future__ import absolute_import

from flytekit.contrib.notebook import python_notebook
from flytekit.sdk.types import Types

interactive_python = python_notebook(notebook_path="../../demo_py_task.ipynb",
                                     inputs={"a": Types.Float, "b": Types.Float},
                                     outputs={"out": Types.Float},
                                     cpu_request="0.5",
                                     memory_request="1G"
                                    )
