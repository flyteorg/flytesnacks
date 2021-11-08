from flytekit.remote import FlyteRemote, workflow_execution

remote = FlyteRemote(
    default_project="flytesnacks",
    default_domain="development",
    flyte_admin_url="localhost:30081",
    insecure=True,
)

flyte_workflow = remote.fetch_workflow(
    name="house_price_prediction.house_price_predictor.house_price_predictor_trainer",
    version="v5",
)

workflow_execution = remote.execute(flyte_workflow, inputs={}, wait=True)
print(workflow_execution.outputs)
