#!/usr/bin/env python3

import datetime
import json
import sys
import time
import traceback
from typing import Dict, List, Mapping, Tuple

import click
import requests
from flytekit.configuration import Config
from flytekit.models.core.execution import WorkflowExecutionPhase
from flytekit.remote import FlyteRemote
from flytekit.remote.executions import FlyteWorkflowExecution

WAIT_TIME = 10
MAX_ATTEMPTS = 200

# This dictionary maps the names found in the flytesnacks manifest to a list of workflow names and
# inputs. This is so we can progressively cover all priorities in the original flytesnacks manifest,
# starting with "core".
FLYTESNACKS_WORKFLOW_GROUPS: Mapping[str, List[Tuple[str, dict]]] = {
    "lite": [
        ("basics.hello_world.hello_world_wf", {}),
    ],
    "core": [
        # ("development_lifecycle.decks.image_renderer_wf", {}),
        # The chain_workflows example in flytesnacks expects to be running in a sandbox.
        ("advanced_composition.chain_entities.chain_workflows_wf", {}),
        ("advanced_composition.dynamics.wf", {"s1": "Pear", "s2": "Earth"}),
        ("advanced_composition.map_task.my_map_workflow", {"a": [1, 2, 3, 4, 5]}),
        # Workflows that use nested executions cannot be launched via flyteremote.
        # This issue is being tracked in https://github.com/flyteorg/flyte/issues/1482.
        # ("control_flow.run_conditions.multiplier", {"my_input": 0.5}),
        # ("control_flow.run_conditions.multiplier_2", {"my_input": 10}),
        # ("control_flow.run_conditions.multiplier_3", {"my_input": 5}),
        # ("control_flow.run_conditions.basic_boolean_wf", {"seed": 5}),
        # ("control_flow.run_conditions.bool_input_wf", {"b": True}),
        # ("control_flow.run_conditions.nested_conditions", {"my_input": 0.4}),
        # ("control_flow.run_conditions.consume_outputs", {"my_input": 0.4, "seed": 7}),
        # ("control_flow.run_merge_sort.merge_sort", {"numbers": [5, 4, 3, 2, 1], "count": 5}),
        ("advanced_composition.subworkflows.parent_workflow", {"my_input1": "hello"}),
        ("advanced_composition.subworkflows.nested_parent_wf", {"a": 3}),
        ("basics.workflow.simple_wf", {"x": [1, 2, 3], "y": [1, 2, 3]}),
        # TODO: enable new files and folders workflows
        # ("basics.files.rotate_one_workflow", {"in_image": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Julia_set_%28C_%3D_0.285%2C_0.01%29.jpg"}),
        # ("basics.folders.download_and_rotate", {}),
        ("basics.hello_world.hello_world_wf", {}),
        ("basics.named_outputs.simple_wf_with_named_outputs", {}),
        # # Getting a 403 for the wikipedia image
        # # ("basics.reference_task.wf", {}),
        ("data_types_and_io.custom_objects.wf", {"x": 10, "y": 20}),
        # Enums are not supported in flyteremote
        # ("type_system.enums.enum_wf", {"c": "red"}),
        ("data_types_and_io.schema.df_wf", {"a": 42}),
        ("data_types_and_io.typed_schema.wf", {}),
        # ("my.imperative.workflow.example", {"in1": "hello", "in2": "foo"}),
    ],
    "integrations-k8s-spark": [
        ("k8s_spark_plugin.pyspark_pi.my_spark", {"triggered_date": datetime.datetime.now()}),
    ],
    "integrations-kfpytorch": [
        ("kfpytorch_plugin.pytorch_mnist.pytorch_training_wf", {}),
    ],
    "integrations-kftensorflow": [
        ("kftensorflow_plugin.tf_mnist.mnist_tensorflow_workflow", {}),
    ],
    # "integrations-pod": [
    #     ("pod.pod.pod_workflow", {}),
    # ],
    "integrations-pandera_examples": [
        ("pandera_plugin.basic_schema_example.process_data", {}),
        # TODO: investigate type mismatch float -> numpy.float64
        # ("pandera_plugin.validating_and_testing_ml_pipelines.pipeline", {"data_random_state": 42, "model_random_state": 99}),
    ],
    "integrations-modin_examples": [
        ("modin_plugin.knn_classifier.pipeline", {}),
    ],
    "integrations-papermilltasks": [
        ("papermill_plugin.simple.nb_to_python_wf", {"f": 3.1415926535}),
    ],
    "integrations-greatexpectations": [
        ("greatexpectations_plugin.task_example.simple_wf", {}),
        ("greatexpectations_plugin.task_example.file_wf", {}),
        ("greatexpectations_plugin.task_example.schema_wf", {}),
        ("greatexpectations_plugin.task_example.runtime_wf", {}),
    ],
}


def execute_workflow(remote, version, workflow_name, inputs):
    print(f"Fetching workflow={workflow_name} and version={version}")
    wf = remote.fetch_workflow(name=workflow_name, version=version)
    return remote.execute(wf, inputs=inputs, wait=False)


def executions_finished(executions_by_wfgroup: Dict[str, List[FlyteWorkflowExecution]]) -> bool:
    for executions in executions_by_wfgroup.values():
        if not all([execution.is_done for execution in executions]):
            return False
    return True


def sync_executions(remote: FlyteRemote, executions_by_wfgroup: Dict[str, List[FlyteWorkflowExecution]]):
    try:
        for executions in executions_by_wfgroup.values():
            for execution in executions:
                print(f"About to sync execution_id={execution.id.name}")
                remote.sync(execution)
    except Exception:
        print(traceback.format_exc())
        print("GOT TO THE EXCEPT")
        print("COUNT THIS!")


def report_executions(executions_by_wfgroup: Dict[str, List[FlyteWorkflowExecution]]):
    for executions in executions_by_wfgroup.values():
        for execution in executions:
            print(execution)


def schedule_workflow_groups(
    tag: str,
    workflow_groups: List[str],
    remote: FlyteRemote,
    terminate_workflow_on_failure: bool,
) -> Dict[str, bool]:
    """
    Schedule workflows executions for all workflow gropus and return True if all executions succeed, otherwise
    return False.
    """
    executions_by_wfgroup = {}
    # Schedule executions for each workflow group,
    for wf_group in workflow_groups:
        workflows = FLYTESNACKS_WORKFLOW_GROUPS.get(wf_group, [])
        executions_by_wfgroup[wf_group] = [
            execute_workflow(remote, tag, workflow[0], workflow[1]) for workflow in workflows
        ]

    # Wait for all executions to finish
    attempt = 0
    while attempt == 0 or (not executions_finished(executions_by_wfgroup) and attempt < MAX_ATTEMPTS):
        attempt += 1
        print(f"Not all executions finished yet. Sleeping for some time, will check again in {WAIT_TIME}s")
        time.sleep(WAIT_TIME)
        sync_executions(remote, executions_by_wfgroup)

    report_executions(executions_by_wfgroup)

    results = {}
    for wf_group, executions in executions_by_wfgroup.items():
        non_succeeded_executions = []
        for execution in executions:
            if execution.closure.phase != WorkflowExecutionPhase.SUCCEEDED:
                non_succeeded_executions.append(execution)
        # Report failing cases
        if len(non_succeeded_executions) != 0:
            print(f"Failed executions for {wf_group}:")
            for execution in non_succeeded_executions:
                print(f"    workflow={execution.spec.launch_plan.name}, execution_id={execution.id.name}")
                if terminate_workflow_on_failure:
                    remote.terminate(execution, "aborting execution scheduled in functional test")
        # A workflow group succeeds iff all of its executions succeed
        results[wf_group] = len(non_succeeded_executions) == 0
    return results


def valid(workflow_group):
    """
    Return True if a workflow group is contained in FLYTESNACKS_WORKFLOW_GROUPS,
    False otherwise.
    """
    return workflow_group in FLYTESNACKS_WORKFLOW_GROUPS.keys()


def run(
    flytesnacks_release_tag: str,
    priorities: List[str],
    config_file_path,
    terminate_workflow_on_failure: bool,
) -> List[Dict[str, str]]:
    remote = FlyteRemote(
        Config.auto(config_file=config_file_path),
        default_project="flytesnacks",
        default_domain="development",
    )

    # For a given release tag and priority, this function filters the workflow groups from the flytesnacks
    # manifest file. For example, for the release tag "v0.2.224" and the priority "P0" it returns [ "core" ].
    manifest_url = (
        "https://raw.githubusercontent.com/flyteorg/flytesnacks/" f"{flytesnacks_release_tag}/flyte_tests_manifest.json"
    )
    r = requests.get(manifest_url)
    parsed_manifest = r.json()
    workflow_groups = []
    workflow_groups = (
        ["lite"]
        if "lite" in priorities
        else [group["name"] for group in parsed_manifest if group["priority"] in priorities]
    )

    results = []
    valid_workgroups = []
    for workflow_group in workflow_groups:
        if not valid(workflow_group):
            results.append(
                {
                    "label": workflow_group,
                    "status": "coming soon",
                    "color": "grey",
                }
            )
            continue
        valid_workgroups.append(workflow_group)

    results_by_wfgroup = schedule_workflow_groups(
        flytesnacks_release_tag, valid_workgroups, remote, terminate_workflow_on_failure
    )

    for workflow_group, succeeded in results_by_wfgroup.items():
        if succeeded:
            background_color = "green"
            status = "passing"
        else:
            background_color = "red"
            status = "failing"

        # Workflow groups can be only in one of three states:
        #   1. passing: this indicates all the workflow executions for that workflow group
        #               executed successfully
        #   2. failing: this state indicates that at least one execution failed in that
        #               workflow group
        #   3. coming soon: this state is used to indicate that the workflow group was not
        #                   implemented yet.
        #
        # Each state has a corresponding status and color to be used in the badge for that
        # workflow group.
        result = {
            "label": workflow_group,
            "status": status,
            "color": background_color,
        }
        results.append(result)
    return results


@click.command()
@click.option(
    "--return_non_zero_on_failure",
    default=False,
    is_flag=True,
    help="Return a non-zero exit status if any workflow fails",
)
@click.option(
    "--terminate_workflow_on_failure",
    default=False,
    is_flag=True,
    help="Abort failing workflows upon exit",
)
@click.argument("flytesnacks_release_tag")
@click.argument("priorities")
@click.argument("config_file")
def cli(
    flytesnacks_release_tag,
    priorities,
    config_file,
    return_non_zero_on_failure,
    terminate_workflow_on_failure,
):
    print(f"return_non_zero_on_failure={return_non_zero_on_failure}")
    results = run(flytesnacks_release_tag, priorities, config_file, terminate_workflow_on_failure)

    # Write a json object in its own line describing the result of this run to stdout
    print(f"Result of run:\n{json.dumps(results)}")

    # Return a non-zero exit code if core fails
    if return_non_zero_on_failure:
        for result in results:
            if result["status"] not in ("passing", "coming soon"):
                sys.exit(1)


if __name__ == "__main__":
    cli()
