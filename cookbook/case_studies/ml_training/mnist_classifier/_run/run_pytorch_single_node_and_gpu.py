from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from pytorch_single_node_and_gpu import pytorch_training_wf

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(pytorch_training_wf)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
