import typing
from datetime import timedelta
from time import sleep

from flytekit import TaskMetadata, task, workflow
from flytekit.extend import Interface, PythonTask, context_manager


# Create a class named `WaitForObjectStoreFile`, which
# derives from `flytekit.PythonFunctionTask` as follows.
class WaitForObjectStoreFile(PythonTask):
    """
    Add documentation here for your plugin.
    This plugin creates an object store file sensor that waits and exits only when the file exists.
    """

    _VAR_NAME: str = "path"

    def __init__(
        self,
        name: str,
        poll_interval: timedelta = timedelta(seconds=10),
        **kwargs,
    ):
        super(WaitForObjectStoreFile, self).__init__(
            task_type="object-store-sensor",
            name=name,
            task_config=None,
            interface=Interface(inputs={self._VAR_NAME: str}, outputs={self._VAR_NAME: str}),
            **kwargs,
        )
        self._poll_interval = poll_interval

    def execute(self, **kwargs) -> typing.Any:
        # No need to check for existence, as that is guaranteed.
        path = kwargs[self._VAR_NAME]
        ctx = context_manager.FlyteContext.current_context()
        user_context = ctx.user_space_params
        while True:
            user_context.logging.info(f"Sensing file in path {path}...")
            if ctx.file_access.exists(path):
                user_context.logging.info(f"file in path {path} exists!")
                return path
            user_context.logging.warning(f"file in path {path} does not exists!")
            sleep(self._poll_interval.seconds)


# Flytekit routes to the right plugin based on the type of `task_config` class if using the `@task` decorator.
# Config is very useful for cases when you want to customize the behavior of the plugin or pass the config information
# to the backend plugin; however, in this case there's no real configuration. The config object can be any class that your
# plugin understands.

# Actual usage
sensor = WaitForObjectStoreFile(
    name="my-objectstore-sensor",
    metadata=TaskMetadata(retries=10, timeout=timedelta(minutes=20)),
    poll_interval=timedelta(seconds=1),
)


@task
def print_file(path: str) -> str:
    print(path)
    return path


@workflow
def my_workflow(path: str) -> str:
    return print_file(path=sensor(path=path))


# Run the workflow locally
if __name__ == "__main__":
    f = "/tmp/some-file"
    with open(f, "w") as w:
        w.write("Hello World!")

    print(my_workflow(path=f))
