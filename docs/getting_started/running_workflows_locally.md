---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

(getting_started_running_workflows_locally)=

# Running workflows locally

TK - "Creating a Flyte project" emphasizes that projects enable you to package code to run on a Flyte cluster, so you would expect this article to mention packaging code (and workflow registration), but it doesn't. We should probably mention those things at least briefly.

## Running a workflow locally (not in a local cluster)

[TK - why run locally + not in a local cluster]

### Prerequisites

* {doc}`Install development tools <installing_development_tools>`
* {doc}`Create a Flyte project <creating_a_flyte_project>` or follow the {doc}`Quickstart guide <quickstart_guide>` to create a standalone workflow file.

### Steps (with example)

(getting_started_running_workflow_local_cluster)=

## Running a workflow in a local cluster

[TK - why run in a local cluster and explanation of demo cluster]

### Prerequisites

* {doc}`Install development tools <installing_development_tools>`
* {doc}`Create a Flyte project <creating_a_flyte_project>` or follow the {doc}`Quickstart guide <quickstart_guide>` to create a standalone workflow file.
* Start Docker

### Steps

First, export the `FLYTECTL_CONFIG` environment variable in your shell:

```{prompt} bash $
export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml
```

Next, start the demo cluster:

```{prompt} bash $
flytectl demo start
```

Run the workflow on the Flyte cluster with `pyflyte run` using the `--remote` flag:

```{prompt} bash $
pyflyte run --remote example.py training_workflow \
--hyperparameters '{"C": 0.1}'
```

You should see a URL to the workflow execution on your demo Flyte cluster. `<execution_name>` is a unique identifier for the workflow execution:

```{prompt} bash $
Go to http://localhost:30080/console/projects/flytesnacks/domains/development/executions/<execution_name> to see execution in the console.
```

Finally, inspect the results by navigating to the URL produced by `pyflyte run` for the workflow execution. You should see FlyteConsole, the web interface used to manage Flyte entities such as tasks, workflows, and executions. The default execution view shows the list of tasks executing in sequential order.

* Clicking on a single task will open a panel that shows task logs, inputs, outputs, and metadata.
* The **Graph** view shows the execution graph of the workflow, providing visual information about the topology of the graph and the state of each node as the workflow progresses.
* On completion, you can inspect the outputs of each task, and ultimately, the overarching workflow.

TK - include separate screenshots for at least the first two bullet points above.

## Next steps

TK
