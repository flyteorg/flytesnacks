from feast_workflow import feast_workflow
from flytekit.configuration import Config
from flytekit.remote import FlyteRemote

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(feast_workflow)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
