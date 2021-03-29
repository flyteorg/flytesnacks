import datetime
import time
from typing import Any

import typing

import flytekit
from flytekit import PythonInstanceTask, workflow, dynamic, LaunchPlan
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
        return {self._VAR: f"{int(self._sleep_time.total_seconds() * 1000)}ms"}

    def execute(self, **kwargs) -> Any:
        time.sleep(self._sleep_time.total_seconds())


tk = SleeperTask(name="second-sleep")


@workflow
def sleeper_workflow():
    tk()


sleeper_lp = LaunchPlan.get_default_launch_plan(flytekit.current_context(), sleeper_workflow)


@dynamic
def launch_n(n: int):
    for i in range(n):
        sleeper_lp()


@dynamic
def launch_m(m: int, n: int):
    for i in range(m):
        launch_n(n=n)


@workflow
def scale_tester(m: int, n: int):
    launch_m(m=m, n=n)


@workflow
def linear_scale_tester(n: int):
    launch_n(n=n)


if __name__ == "__main__":
    scale_tester(m=5, n=2)
