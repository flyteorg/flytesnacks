---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

(getting_started_quickstart_guide)=

# Quickstart guide

In this guide, you will create and run a Flyte workflow composed of Flyte tasks to generate the output “Hello, World!”.

## Prerequisites

* Install Python (TK - what version?)
* Install Flytekit with `pip install flytekit`

## Steps

### Create a workflow

First, create a file called `hello_world.py` and copy the following code into the file:

```python
from flytekit import task, workflow

@task
def say_hello() -> str:
    return "Hello, World!"

@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res

if __name__ == "__main__":
    print(f"Running hello_world_wf() {hello_world_wf()}")
```

### Run the workflow

Next, run the workflow with `pyflyte run`:

```{prompt} bash
pyflyte run hello_world.py hello_world_wf
```

:::{note}
The initial arguments of `pyflyte run` take the form of
`path/to/script.py <task_or_workflow_name>`, where `<task_or_workflow_name>`
refers to the function decorated with `@task` or `@workflow` that you wish to run.
:::

## The @task and @workflow decorators

In this example, the workflow file `hello_world.py` contains tasks and a workflow, decorated with the `@task` and `@workflow` decorators, respectively. You can invoke tasks and workflows like regular Python methods, and even import and use them in other Python modules or scripts.

To learn more about tasks and workflows, see the {ref}`"Workflow code" section<getting_started_workflow_code>` of {ref}`"Flyte project components"<getting_started_flyte_project_components>`.

### @task

The @task decorator indicates functions that define tasks:

* A task is a Python function that takes some inputs and produces an output.
* When deployed to a Flyte cluster, each task runs in its own Kubernetes pod.
* Tasks are assembled into workflows.

For more information on tasks, see "TK - link to eventual task feature/concept doc".

### @workflow

The @workflow decorator indicates a function-esque construct that defines a workflow

* Workflows specify the flow of data between tasks, and the dependencies between tasks.
* A workflow appears to be a Python function but is actually a DSL that only supports a subset of Python syntax and semantics.
* When deployed to a Flyte cluster the workflow function is "compiled" to construct the directed acyclic graph (DAG) of tasks, defining the order of execution of task pods and the data flow dependencies between them. TK - what part of the data plane does the compiling?

For more information on workflows, see "TK - link to workflow concept / feature doc".

## Next steps

To create a Flyte Project and run the workflow in a local Flyte cluster, see {ref}`"Getting started with workflow development"<getting_started_with_workflow_development>`.
