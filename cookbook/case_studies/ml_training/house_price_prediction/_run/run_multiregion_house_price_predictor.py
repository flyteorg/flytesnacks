from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from multiregion_house_price_predictor import multi_region_house_price_prediction_model_trainer

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(
    multi_region_house_price_prediction_model_trainer
)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
