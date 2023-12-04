---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

# Running a workflow locally

[TK - "Creating a Flyte project" emphasizes that projects enable you to package code to run on a Flyte cluster, so you would expect this article to mention packaging code (and workflow registration), but it doesn't. We should probably mention those things at least briefly.]

## Running a workflow in a local Python environment

To quickly test changes to workflow code without the overhead of running a local cluster, you can run a workflow in a local Python environment.

[TK - either include a note about the limitations of this approach or remove this section, make the entire article about running a workflow in a local cluster, and add a note about how you can run in a local Python environment as well, but that is not a recommended approach]

### Prerequisites

* {doc}`Install development tools <installing_development_tools>`
* {doc}`Create a Flyte project <creating_a_flyte_project>`

### Steps

1. On the command line, navigate to the workflows directory of your Flyte project:
```{prompt} bash $
cd my_project/workflows
```
2. Run the workflow on the Flyte cluster with `pyflyte run`:
```{prompt} bash $
pyflyte run --remote example.py wf
```

(getting_started_running_workflow_local_cluster)=

## Running a workflow in a local cluster

To test changes to workflow code in a production-like environment, you can run a workflow in a local Flyte cluster.

### Prerequisites

* {doc}`Install development tools <installing_development_tools>`
* {doc}`Create a Flyte project <creating_a_flyte_project>`
* Start the Docker daemon

### Steps

1. Export the `FLYTECTL_CONFIG` environment variable in your shell:

```{prompt} bash $
export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml
```
2. Start the demo cluster:

```{prompt} bash $
flytectl demo start
```
3. On the command line, navigate to the workflows directory of your Flyte project:
```{prompt} bash $
cd my_project/workflows
```
4. Run the workflow on the Flyte cluster with `pyflyte run` using the `--remote` flag:
```{prompt} bash $
pyflyte run --remote example.py wf
```

You should see a URL to the workflow execution on your demo Flyte cluster, where `<execution_name>` is a unique identifier for the workflow execution:

```{prompt} bash $
Go to http://localhost:30080/console/projects/flytesnacks/domains/development/executions/<execution_name> to see execution in the console.
```

:::{note}
In this example, you can also pass a `name` parameter to the workflow:

```{prompt} bash $
pyflyte run --remote example.py wf --name Ada
```
:::

### Inspecting the results of the workflow run

You can inspect the results of a workflow run by navigating to the URL produced by `pyflyte run` for the workflow execution. You should see FlyteConsole, the web interface used to manage Flyte entities such as tasks, workflows, and executions. The default execution view shows the list of tasks executing in sequential order.

![](https://raw.githubusercontent.com/flyteorg/static-resources/nikki-onboarding-docs-revamp/flytesnacks/getting_started/flyteconsole_default.png)

Clicking on a single task will open a panel that shows task logs, inputs, outputs, and metadata.
![](https://raw.githubusercontent.com/flyteorg/static-resources/nikki-onboarding-docs-revamp/flytesnacks/getting_started/flyteconsole_task_panel.png)

The **Graph** view shows the execution graph of the workflow, providing visual information about the topology of the graph and the state of each node as the workflow progresses.

![](https://raw.githubusercontent.com/flyteorg/static-resources/nikki-onboarding-docs-revamp/flytesnacks/getting_started/flyteconsole_graph_view.png)

On completion, you can inspect the outputs of each task, and ultimately, the overarching workflow.
