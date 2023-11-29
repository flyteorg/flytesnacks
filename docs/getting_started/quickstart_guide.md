---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst

# override the toc-determined page navigation order
prev-page: index
prev-page-title: Introduction to Flyte
next-page: getting_started/getting_started_with_workflow_development
next-page-title: Getting started with workflow development
---

(getting_started_quickstart_guide)=

# Quickstart guide

In this guide, you will create and run a Flyte workflow to generate the output “Hello, World!”.

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

In this example, the file `hello_world.py` contains a task and a workflow, decorated with the `@task` and `@workflow` decorators, respectively. You can invoke tasks and workflows like regular Python methods, and even import and use them in other Python modules or scripts.

To learn more about tasks and workflows, see the {ref}`"Workflow code" section<getting_started_workflow_code>` of {ref}`"Flyte project components"<getting_started_flyte_project_components>`.

## Next steps

To create a Flyte project that can be used to package workflow code for deployment to a Flyte cluster, see {ref}`"Getting started with workflow development" <getting_started_with_workflow_development>`
