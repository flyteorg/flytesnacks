from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from keras_spark_rossmann_estimator import horovod_spark_wf

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flytesnacks",
    default_domain="development",
)

registered_workflow = remote.register_script(horovod_spark_wf)

execution = remote.execute(registered_workflow, inputs={})
print(f"Execution successfully started: {execution.id.name}")
