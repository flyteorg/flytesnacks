import datetime
import time
from typing import Any

import typing
from flytekit import PythonInstanceTask, workflow, dynamic
from flytekit.core.context_manager import SerializationSettings
from flytekit.extend import Interface


class SleeperTask(PythonInstanceTask):
    _VAR = "sleep"

    def __init__(self, name: str, sleep_time: typing.Optional[datetime.timedelta] = None, **kwargs):
        super().__init__(task_type="sleep", task_config=None, name=name, interface=Interface(inputs={}, outputs={}),
                         **kwargs)
        if sleep_time:
            self._sleep_time = sleep_time
        else:
            self._sleep_time = datetime.timedelta(seconds=1)

    def get_config(self, settings: SerializationSettings) -> typing.Dict[str, str]:
        return {self._VAR: f"{int(self._sleep_time.total_seconds() * 1000)  }ms"}

    def execute(self, **kwargs) -> Any:
        time.sleep(self._sleep_time.total_seconds())


tk = SleeperTask(name="second-sleep")


@workflow
def sleeper_workflow():
    tk()


@dynamic
def launch_n(n: int):
    for i in range(n):
        sleeper_workflow()


@workflow
def scale_tester(n: int):
    launch_n(n=n)


if __name__ == "__main__":
    scale_tester(n=2)
