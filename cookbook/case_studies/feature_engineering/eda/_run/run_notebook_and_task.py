from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from notebook_and_task import notebook_wf

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(notebook_wf)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
