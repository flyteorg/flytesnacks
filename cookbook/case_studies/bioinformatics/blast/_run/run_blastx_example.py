from blastx_example import blast_wf
from flytekit.configuration import Config
from flytekit.remote import FlyteRemote

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(blast_wf)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
