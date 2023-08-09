import typing
from collections import OrderedDict

import pytest
from flyteidl.artifact import artifacts_pb2
from flyteidl.core import identifier_pb2
from typing_extensions import Annotated

from flytekit.configuration import Config, Image, ImageConfig, SerializationSettings
from flytekit.core.artifact import Artifact
from flytekit.core.context_manager import FlyteContextManager
from flytekit.core.launch_plan import LaunchPlan
from flytekit.core.task import task
from flytekit.core.workflow import workflow
from flytekit.remote.remote import FlyteRemote
from flytekit.tools.translator import get_serializable
from flytekit.types.structured.structured_dataset import StructuredDataset
from examples.artifacts import ml_demo

r = FlyteRemote(
    Config.auto(config_file="/Users/ytong/.flyte/local_admin.yaml"),
    default_project="flytesnacks",
    default_domain="development",
)


def test_work_with_artifacts_locally():
    # Getting it the old way, through tiny url
    # out = r.client.get_data("flyte://v1/flytesnacks/development/a5zk94pb6lgg5v7l7zw8/n0/0/o0")
    # print(out)
    # Getting it the new way, through the artifact object
    """
        def get_artifact(
        self,
        uri: typing.Optional[str] = None,
        artifact_key: typing.Optional[identifier_pb2.ArtifactKey] = None,
        artifact_id: typing.Optional[identifier_pb2.ArtifactID] = None,
        query: typing.Optional[identifier_pb2.ArtifactQuery] = None,
        get_details: bool = False,
    ) -> typing.Optional[artifacts_pb2.Artifact]:
    """
    r.get_artifact(uri="flyte://av0.1/flytesnacks/development/a5zk94pb6lgg5v7l7zw8/n0/0/o:o0")



def test_kljkljl():
    # def my_wf(a: int, b: str) -> Tuple[int, str]:
    wf = r.fetch_workflow(
        "flytesnacks", "development", "cookbook.core.flyte_basics.basic_workflow.my_wf", "KVBL7dDsBdtaqjUgZIJzdQ=="
    )

    a = r.get_artifact(uri="flyte://av0.1/flytesnacks/development/flyteorg.test.yt.test1:v0.1.6")
    print(a)
    r.execute(wf, inputs={"a": a})


def test_perm():
    x = ml_demo.get_permutations("SEA")
    print(x)
