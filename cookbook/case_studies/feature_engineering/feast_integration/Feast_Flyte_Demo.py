"""
How to Trigger the Feast Workflow using FlyteRemote
===================================================

The goal of this notebook is to train a simple `Gaussian Naive Bayes
model using
sklearn <https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html>`__
on a modified `Horse-Colic dataset from
UCI <https://archive.ics.uci.edu/ml/datasets/Horse+Colic>`__.

The model aims to classify if the lesion of the horse is surgical or
not.

Let’s get started!

"""


######################################################################
# Set the AWS environment variables before importing Flytekit.
#

import os

os.environ["FLYTE_AWS_ENDPOINT"] = os.environ[
    "FEAST_S3_ENDPOINT_URL"
] = "http://localhost:30084/"
os.environ["FLYTE_AWS_ACCESS_KEY_ID"] = os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["FLYTE_AWS_SECRET_ACCESS_KEY"] = os.environ[
    "AWS_SECRET_ACCESS_KEY"
] = "miniostorage"


######################################################################
# 01. Register the code
# ~~~~~~~~~~~~~~~~~~~~~
#
# The actual workflow code is auto-documented and rendered using sphinx
# `here <https://docs.flyte.org/projects/cookbook/en/latest/auto/case_studies/feature_engineering/feast_integration/index.html>`__.
# We’ve used
# `Flytekit <https://docs.flyte.org/projects/flytekit/en/latest/>`__ to
# express the pipeline in pure Python.
#
# You can use `FlyteConsole <https://github.com/flyteorg/flyteconsole>`__
# to launch, monitor, and introspect Flyte executions. However here, let’s
# use
# `flytekit.remote <https://docs.flyte.org/projects/flytekit/en/latest/design/control_plane.html>`__
# to interact with the Flyte backend.
#

from flytekit.configuration import Config
from flytekit.remote import FlyteRemote

# The `for_sandbox` method instantiates a connection to the demo cluster.
remote = FlyteRemote(
    config=Config.for_sandbox(),
    default_project="flytesnacks",
    default_domain="development",
)


######################################################################
# The ``register_script`` method can be used to register the workflow.
#

from feast_workflow import feast_workflow
from flytekit.configuration import ImageConfig

if os.getenv("SANDBOX") is None:
    wf = remote.register_script(
        feast_workflow,
        image_config=ImageConfig.from_images(
            "ghcr.io/flyteorg/flytecookbook:feast_integration-latest"
        ),
        version="v2",
        source_path="../",
        module_name="feast_workflow",
    )
else:
    wf = remote.register_script(
        feast_workflow,
        image_config=ImageConfig.from_images(
            "ghcr.io/flyteorg/flytecookbook:feast_integration-latest"
        ),
        version="v1",
        source_path=".",
        module_name="feast_workflow",
    )


######################################################################
# 02: Launch an execution
# ~~~~~~~~~~~~~~~~~~~~~~~
#


######################################################################
# FlyteRemote provides convenient methods to retrieve version of the
# pipeline from the remote server.
#
# **NOTE**: It is possible to get a specific version of the workflow and
# trigger a launch for that, but let’s just get the latest.
#

lp = remote.fetch_launch_plan(name="feast_integration.feast_workflow.feast_workflow")
lp.id.version


######################################################################
# The ``execute`` method can be used to execute a Flyte entity — a launch
# plan in our case.
#

execution = remote.execute(lp, inputs={"num_features_univariate": 5}, wait=True)


######################################################################
# 03. Sync an execution
# ~~~~~~~~~~~~~~~~~~~~~
#
# You can sync an execution to retrieve the workflow’s outputs.
# ``sync_nodes`` is set to True to retrieve the intermediary nodes’
# outputs as well.
#
# **NOTE**: It is possible to fetch an existing execution or simply
# retrieve an already commenced execution. Also, if you launch an
# execution with the same name, Flyte will respect that and not restart a
# new execution!
#

from flytekit.models.core.execution import WorkflowExecutionPhase

synced_execution = remote.sync(execution, sync_nodes=True)
print(
    f"Execution {synced_execution.id.name} is in {WorkflowExecutionPhase.enum_to_string(synced_execution.closure.phase)} phase"
)


######################################################################
# 04. Retrieve the output
# ~~~~~~~~~~~~~~~~~~~~~~~
#
# Fetch the model and the model prediction.
#

model = synced_execution.outputs["o0"]
prediction = synced_execution.outputs["o1"]
prediction


######################################################################
# **NOTE**: The output model is available locally as a JobLibSerialized
# file, which can be downloaded and loaded.
#

model


######################################################################
# Fetch the ``repo_config``.
#

repo_config = synced_execution.node_executions["n0"].outputs["o0"]


######################################################################
# 05. Generate predictions
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# Re-use the ``predict`` function from the workflow to generate
# predictions — Flytekit will automatically manage the IO for you!
#


######################################################################
# Load features from the online feature store
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#

import os

from feast_workflow import FEAST_FEATURES, predict, retrieve_online

inference_point = retrieve_online(
    repo_config=repo_config,
    online_store=synced_execution.node_executions["n4"].outputs["o0"],
    data_point=533738,
)
inference_point


######################################################################
# Generate a prediction
# ^^^^^^^^^^^^^^^^^^^^^
#

predict(model_ser=model, features=inference_point)
