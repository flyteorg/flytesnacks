import datetime
import time
import subprocess
import pytest
import core as c

from flytekit.remote.remote import FlyteRemote
from flytekit.common.exceptions.user import FlyteAssertion

PROJECT = "flytesnacks"
DOMAIN = "development"
VERSION = "latest"
FLYTE_TEST_MANIFEST_PATH = '../flyte_tests_manifest.json'

class TestManifest:
    __test__ = False

    name: str
    type: str
    priority: str
    data: dict
    exitCondition: dict
    response: dict

    def __init__(self, name, manifest):
        self.name = name
        self.type = manifest["type"]
        self.priority = manifest["priority"]
        self.data = manifest["data"]
        self.exitCondition = manifest["exitCondition"]

    async def register_workflow(self):
        remote = FlyteRemote()
        lp = remote.fetch_launch_plan(
            project=PROJECT, domain=DOMAIN, name=self.name, version=VERSION
        )
        self.response = lp

    async def run_launch_plan(self):
        remote = FlyteRemote()
        lp = remote.fetch_launch_plan(
            project=PROJECT, domain=DOMAIN, name=self.name, version=VERSION
        )
        execution = remote.execute(lp, self.data["input"])
        execution.wait_for_completion()
        self.response = execution

    async def fetch_execute_task(self):
        remote = FlyteRemote()
        flyte_task = remote.fetch_task(PROJECT, DOMAIN, self.name, VERSION)
        execution = remote.execute(flyte_task, self.data["input"])
        execution.wait_for_completion()
        self.response = execution

    async def monitor_workflow_execution(self):
        remote = FlyteRemote()
        flyte_launch_plan = remote.fetch_launch_plan(
            PROJECT, DOMAIN, self.name, VERSION
        )
        print(self.data["input"])
        execution = remote.execute(flyte_launch_plan, self.data["input"])

        poll_interval = datetime.timedelta(seconds=1)
        time_to_give_up = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)

        execution.sync()
        while datetime.datetime.utcnow() < time_to_give_up:

            if execution.is_complete:
                execution.sync()
                break

            with pytest.raises(
                FlyteAssertion, match="Please wait until the node execution has completed before requesting the outputs"
            ):
                execution.outputs

            time.sleep(poll_interval.total_seconds())
            execution.sync()

            if execution.node_executions:
                assert execution.node_executions["start-node"].closure.phase == 3  # SUCCEEEDED
        self.response = execution


@pytest.fixture(scope="session")
def flyte_workflows_register(request):
    print("Hello")
    subprocess.check_call(
        f"flytectl register example -p {PROJECT} -d {DOMAIN} --version={VERSION}",
        shell=True,
    )


def get_test_manifest():
    return c.TEST_MANIFEST


def filter_results(test_test: str):
    results = []
    test_data = get_test_manifest()
    for name in test_data:
        manifest = TestManifest(name, test_data[name])
        if manifest.type == test_test:
            results.append(manifest)
    return results


