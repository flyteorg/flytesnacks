import flytekit.configuration
from flytekit import Resources
from flytekit.configuration import Image, ImageConfig
from flytekit.core.python_auto_container import default_task_resolver
from flytekit.core.python_function_task import PythonFunctionTask
from flytekit.core.task import task

from core.ta_main import generate_dataset
from core.ta_main import train_model as tmodel

default_img = Image(name="default", fqn="test", tag="tag")
serialization_settings = flytekit.configuration.SerializationSettings(
    project="project",
    domain="domain",
    version="version",
    env=None,
    image_config=ImageConfig(default_image=default_img, images=[default_img]),
)


generate_dataset_task = task(requests=Resources(cpu="1"), limits=Resources(cpu="1"), retries=3)(generate_dataset)
train_model_task = task(requests=Resources(cpu="1"), limits=Resources(cpu="1"), retries=3)(tmodel)


if __name__ == "__main__":
    print(isinstance(train_model_task, PythonFunctionTask))

    xx = default_task_resolver.loader_args(serialization_settings, train_model_task)
    print(xx)

