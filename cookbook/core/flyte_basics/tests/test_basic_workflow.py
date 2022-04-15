from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from flytekit.tools.translator import Options

from core.extend_flyte.run_custom_types import wf

remote = FlyteRemote(
    config=Config.for_endpoint("localhost:30080"),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(
    wf, options=Options.default_from(k8s_service_account="demo")
)

remote.execute(
    registered_workflow,
    inputs={},
)
