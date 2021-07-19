import pytest
import utils as u

PROJECT = "flytesnacks"
DOMAIN = "development"
VERSION = "latest"
FLYTE_TEST_MANIFEST_PATH = '../flyte_tests_manifest.json'


async def assert_workflow_register(manifest):
    assert manifest.response.id.name == manifest.name
    assert manifest.response.id.project == PROJECT
    assert manifest.response.id.domain == DOMAIN


async def assert_workflow(manifest):
    if manifest.name == "core.flyte_basics.files.rotate_one_workflow" \
            or manifest.name == "core.flyte_basics.folders.download_and_rotate":
        assert manifest.response.closure.outputs.uri[:5] == "s3://"
    else:
        assert manifest.response.outputs == manifest.data["output"]


async def assert_monitor_workflow(manifest):
    for key in manifest.response.node_executions:
        assert manifest.response.node_executions[key].closure.phase == 3

    if manifest.name == "core.flyte_basics.files.rotate_one_workflow" \
            or manifest.name == "core.flyte_basics.folders.download_and_rotate":
        assert manifest.response.closure.outputs.uri[:5] == "s3://"
    else:
        if 'n0' in manifest.data:
            assert manifest.response.node_executions["n0"].inputs == manifest.data["n0"]["input"]
            assert manifest.response.node_executions["n0"].outputs == manifest.data["n0"]["output"]
            assert manifest.response.node_executions["n0"].task_executions[0].inputs == manifest.data["n0"]["input"]
            assert manifest.response.node_executions["n0"].task_executions[0].outputs == manifest.data["n0"]["output"]
        if 'n1' in manifest.data:
            assert manifest.response.node_executions["n1"].inputs == manifest.data["n1"]["input"]
            assert manifest.response.node_executions["n1"].outputs == manifest.data["n1"]["output"]
            assert manifest.response.node_executions["n1"].task_executions[0].inputs == manifest.data["n1"]["input"]
            assert manifest.response.node_executions["n1"].task_executions[0].outputs == manifest.data["n1"]["output"]


@pytest.mark.asyncio
async def test_fetch_execute_task(flyteclient, flyte_workflows_register):
    for manifest in u.filter_results("task"):
        print(f"Running {manifest.type} for {manifest.name}")
        await manifest.fetch_execute_task()
        await assert_workflow(manifest)


@pytest.mark.asyncio
async def test_run_launch_plan(flyteclient, flyte_workflows_register):
    for manifest in u.filter_results("lp"):
        print(f"Running {manifest.type} for {manifest.name}")
        await manifest.run_launch_plan()
        await assert_workflow(manifest)


@pytest.mark.asyncio
async def test_monitor_workflow_execution(flyteclient, flyte_workflows_register):
    for manifest in u.filter_results("lp"):
        print(f"Running {manifest.type} for {manifest.name}")
        await manifest.monitor_workflow_execution()
        await assert_monitor_workflow(manifest)


@pytest.mark.asyncio
async def test_register_workflow(flyteclient, flyte_workflows_register):
    for manifest in u.filter_results("lp"):
        print(f"Running {manifest.type} for {manifest.name}")
        await manifest.register_workflow()
        await assert_workflow_register(manifest)

