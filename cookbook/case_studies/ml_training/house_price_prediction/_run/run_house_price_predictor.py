from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from house_price_predictor import house_price_predictor_trainer

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(house_price_predictor_trainer)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
