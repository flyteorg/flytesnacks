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

In this guide, you will create and run a Flyte workflow in a local Python environment to generate the output "Hello, World!"

## Prerequisites

* [Download Python 3.8x or higher](https://www.python.org/downloads/)
* [Download `pip`](https://pip.pypa.io/en/stable/installation/)
* Install [Flytekit](https://github.com/flyteorg/flytekit) with `pip install -U flytekit`

## Steps

### Create a workflow

First, create a file called `hello_world.py` and copy the following code into the file:

```python
from flytekit import task, workflow

@task
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

@workflow
def hello_world_wf(name: str = 'world') -> str:
    res = say_hello(name=name)
    return res
```

### Run the workflow in a local Python environment

Next, run the workflow with `pyflyte run`. The initial arguments of `pyflyte run` take the form of
`path/to/script.py <task_or_workflow_name>`, where `<task_or_workflow_name>`
refers to the function decorated with `@task` or `@workflow` that you wish to run:

```{prompt} bash
pyflyte run hello_world.py hello_world_wf
```

You can also provide a `name` argument to the workflow:
```{prompt} bash
pyflyte run hello_world.py hello_world_wf --name Ada
```

:::{note}
While you can run the example file like a Python script with `python hello_world.py`, we recommend using `pyflyte run` instead. To run the file like a Python script, you would have to add a `main` module conditional at the end of the script:
```python
if __name__ == "__main__":
    print(hello_world_wf())
```

Your code would become even more verbose if you wanted to pass arguments to the workflow:
```python
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--name", type=str)

    args = parser.parse_args()
    print(hello_world_wf(name=args.name))
```
:::

## The @task and @workflow decorators

In this example, the file `hello_world.py` contains a task and a workflow, decorated with the `@task` and `@workflow` decorators, respectively. You can invoke tasks and workflows like regular Python methods, and even import and use them in other Python modules or scripts.

To learn more about tasks and workflows, see the {ref}`"Workflow code" section<getting_started_workflow_code>` of {doc}`"Flyte project components"<flyte_project_components>`.

## Next steps

To create a Flyte project to structure your workflow code according to software engineering best practices, and can be used to package workflow code for deployment to a Flyte cluster, see {doc}`"Getting started with workflow development" <getting_started_with_workflow_development>`
