from flytekit import kwtypes, task, workflow, dynamic
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema

from flytekitplugins.athena import AthenaTask, AthenaConfig


def generate_and_register_feature_eng_pipeline(name: str, query: str, inputs: Dict[str, Type]) -> Workflow:
    a = AthenaTask(query_template=query, inputs=inputs)
    wb = WorkflowBuilder(f"feature-{name}-pipeline")
    wb.add_task(a)
    wb.add_task(ReferenceTask("appleproject1", "development", "data_imputer", "latest"))
    w = wb.build()
    register(w)


generate_feature_eng_pipeline("my-feature", "Select * from vaccinations where x= {{.inputs.x}}", {x: int})
