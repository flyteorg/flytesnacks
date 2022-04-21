"""
.. _hosted_multi_images:

Multiple Container Images in a Single Workflow
----------------------------------------------

When working locally, it is recommended to install all requirements of your project locally (maybe in a single virtual environment). It gets complicated when you want to deploy your code to a remote
environment. This is because most tasks in Flyte (function tasks) are deployed using a Docker Container. 

A Docker container allows you to create an expected environment for your tasks. It is also possible to build a single container image with all your dependencies, but is complicated to achieve in practice.

Here are the reasons why it is complicated and not recommended:

#. All the dependencies in one container increase the size of the container image.
#. Some task executions like Spark, Sagemaker-based Training, and Deep Learning use GPUs that need specific runtime configurations. For example,
   
   - Spark needs JavaVirtualMachine installation and Spark entrypoints to be set
   - NVIDIA drivers and corresponding libraries need to be installed to use GPUs for deep learning. However, these are not required for a CPU
   - Sagemaker expects the entrypoint to be designed to accept its parameters

#. Building a single image may increase the build time for the image itself.

.. note::

   Flyte (Service) by default does not require a workflow to be bound to a single container image. Flytekit offers a simple interface to easily alter the images that should be associated for every task, yet keeping the local execution simple for the user.


For every :py:class:`flytekit.PythonFunctionTask` type task or simply a task that is decorated with the ``@task`` decorator, users can supply rules of how the container image should be bound. By default, flytekit will associate one container image with all tasks. This image is called the ``default`` image.
To alter the image, users should use the ``container_image`` parameter available in the :py:func:`flytekit.task` decorator. Any one of the following is an acceptable

#. Image reference is specified, but the version is derived from the default images version ``container_image="docker.io/redis:{{.image.default.version}},``
#. Both the FQN and the version are derived from the default image ``container_image="{{.image.default.fqn}}:spark-{{.image.default.version}},``

The images themselves are parameterizable in the config in the following format:
 ``{{.image.<name>.<attribute>}}``

- ``name`` refers to the name of the image in the image configuration. The name ``default`` is a reserved keyword and will automatically apply to the default image name for this repository.
- ``fqn`` refers to the fully qualified name of the image. For example it includes the repository and domain url of the image. E.g. docker.io/my_repo/xyz.
- ``version`` refers to the tag of the image. E.g. latest, or python-3.8 etc. If the container_image is not specified then the default configured image for the project is used.

.. note::

    The default image (name + version) is always ``{{.image.default.fqn}}:{{.image.default.version}}``

.. warning:

    It is the responsibility of the user to push a container image that matches the new name described.

Let us understand how multiple images can be used within a single workflow using an example.
"""
# %%
# Import the necessary dependencies. 
from flytekit import task, workflow
import pandas as pd
from typing import NamedTuple
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

split_data = NamedTuple(
    "split_data",
    train_features=pd.DataFrame,
    test_features=pd.DataFrame,
    train_labels=pd.DataFrame,
    test_labels=pd.DataFrame,
)

# %%
# Define a task that fetches data and splits the data into train and test sets.
@task(container_image="smritisatyan/multi-images-preprocess:latest")
def svm_trainer() -> split_data:
    dataset_url = "https://raw.githubusercontent.com/harika-bonthu/SupportVectorClassifier/main/datasets_229906_491820_Fish.csv"
    fish_data = pd.read_csv(dataset_url)   
    X = fish_data.drop(['Species'], axis = 'columns')
    y = fish_data.Species
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.31)
    y_train = y_train.to_frame()
    y_test = y_test.to_frame()

    return split_data(
        train_features=X_train,
        test_features=X_test,
        train_labels=y_train,
        test_labels=y_test,
    )
    
# %%
# Define another task that trains the model on the data and computes the accuracy score.
@task(container_image="smritisatyan/multi-images-predict:latest") 
def svm_predictor(X_train:pd.DataFrame,X_test:pd.DataFrame,y_train:pd.DataFrame,y_test:pd.DataFrame) -> float:
    model = SVC(kernel = 'linear', C = 1)
    model.fit(X_train, y_train.values.ravel()) 
    svm_pred = model.predict(X_test)
    accuracy_score = model.score(X_test, y_test.values.ravel())
    return accuracy_score

# %%
# Define a workflow.
@workflow
def my_workflow() -> float:
    train_model = svm_trainer()
    svm_accuracy = svm_predictor(X_train = train_model.train_features, 
                                 X_test = train_model.test_features,
                                 y_train = train_model.train_labels,
                                 y_test = train_model.test_labels)
    return svm_accuracy
    
    
if __name__ == "__main__":
    print(f"Running my_workflow(), accuracy : { my_workflow() }")

# %%
# .. note::
#     Notice that the two task annotators have two different `container_image` specified.
