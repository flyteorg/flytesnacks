"""
ScikitLearn Example
-------------------

In this example, we will see how to convert a scikitlearn model to an ONNX model.

First import the necessary libraries.
"""
from typing import List, NamedTuple

import numpy
import onnxruntime as rt
import pandas as pd
from flytekit import task, workflow
from flytekit.types.file import ONNXFile
from flytekitplugins.onnxscikitlearn import ScikitLearn2ONNX, ScikitLearn2ONNXConfig
from skl2onnx.common.data_types import FloatTensorType
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from typing_extensions import Annotated

# %%
# Define a ``NamedTuple`` to hold the output schema.
# Note the annotation on the ``model`` field.
# This is a special annotation that tells Flytekit that this parameter is to be converted to an ONNX model with the given metadata.
TrainOutput = NamedTuple(
    "TrainOutput",
    [
        (
            "model",
            Annotated[
                ScikitLearn2ONNX,
                ScikitLearn2ONNXConfig(
                    initial_types=[("float_input", FloatTensorType([None, 4]))],
                    target_opset=12,
                ),
            ],
        ),
        ("test", pd.DataFrame),
    ],
)

# %%
# The acceptable parameters for the ``ScikitLearn2ONNXConfig`` dataclass are as follows:
#
# .. list-table:: ``ScikitLearn2ONNXConfig`` Parameters
#
#   * - ``initial_types``
#     - ``list[tuple[str, type]]``
#     - The types of the inputs to the model.
#   * - ``name``
#     - ``str``
#     - The name of the graph in the produced ONNX model.
#   * - ``doc_string``
#     - ``str``
#     - A string attached onto the produced ONNX model.
#   * - ``target_opset``
#     - ``int``
#     - The ONNX opset number.
#   * - ``custom_conversion_functions``
#     - ``dict[Callable[..., Any], Callable[...,  None]]``
#     - A dictionary for specifying the user customized conversion function.
#   * - ``custom_shape_calculators``
#     - ``dict[Callable[..., Any], Callable[...,  None]]``
#     - A dictionary for specifying the user customized shape calculator.
#   * - ``custom_parsers``
#     - ``dict[Callable[..., Any], Callable[...,  None]]``
#     - Parsers determine which outputs are expected for which particular task.
#   * - ``options``
#     - ``dict[Any, Any]``
#     - Specific options given to converters.
#   * - ``intermediate``
#     - ``bool``
#     - If True, the function returns the converted model and the instance of Topology used, else, it returns the converted model.
#   * - ``naming``
#     - ``Union[str, Callable[..., Any]]``
#     - Change the way intermediates are named.
#   * - ``white_op``
#     - ``set[str]``
#     - White list of ONNX nodes allowed while converting a pipeline.
#   * - ``black_op``
#     - ``set[str]``
#     - Black list of ONNX nodes disallowed while converting a pipeline.
#   * - ``verbose``
#     - ``int``
#     - Display progress while converting a model
#   * - ``final_types``
#     - ``list[tuple[str, type]]``
#     - Used to overwrite the type (if type is not None) and the name of every output.

# %%
# Define a ``train`` task that will train a scikitlearn model and return the model and test data.
@task
def train() -> TrainOutput:
    iris = load_iris(as_frame=True)
    X, y = iris.data, iris.target
    X_train, X_test, y_train, _ = train_test_split(X, y)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return TrainOutput(test=X_test, model=ScikitLearn2ONNX(model))


# %%
# Define a ``predict`` task that will use the model to predict the labels for the test data.
@task
def predict(
    model: ONNXFile,
    X_test: pd.DataFrame,
) -> List[int]:
    sess = rt.InferenceSession(model.download())
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred_onx = sess.run(
        [label_name], {input_name: X_test.to_numpy(dtype=numpy.float32)}
    )[0]
    return pred_onx.tolist()


# %%
# Lastly define a workflow to run the above tasks.
@workflow
def wf() -> List[int]:
    train_output = train()
    return predict(model=train_output.model, X_test=train_output.test)


# %%
# Run the workflow locally.
if __name__ == "__main__":
    print(f"Predictions: {wf()}")
