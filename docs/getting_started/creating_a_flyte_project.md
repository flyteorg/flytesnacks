---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

(getting_started_creating_a_flyte_project)=

# Creating a Flyte Project

## About Flyte Projects

[TK - link to repo with project templates]

## Prerequisites

* Follow the steps in "[Installing development tools](#)"
* Install git

## Steps

1. Create a virtual environment with conda (or other tool) to manage dependencies. [TK - if we want people to install flytekit after creating a virtual env, they need to do that after this step]
2. Initialize your Flyte project [TK - slope/intercept example]
3. Install additional requirements with `pip install -r requirements.txt`.
4. Initialize git repository in your Flyte project directory.
5. Create at least one commit so you can later register the workflow to the local Flyte cluster.

```{note}
TK - benefits of versioning your project.
```

## Flyte Project components

### Directory structure and configuration files

[TK - dir structure and config files]

### Workflow code

In this example, the workflow file [TK - name of file] contains tasks and a workflow, decorated with the `@task` and `@workflow` decorators, respectively. You can invoke tasks and workflows like regular Python methods, and even import and use them in other Python modules or scripts.

[TK - example workflow code]

#### @task

The @task decorator indicates functions that define tasks:

* A task is a Python function that takes some inputs and produces an output.
* When deployed to a Flyte cluster, each task runs in its own Kubernetes pod.
* Tasks are assembled into workflows.

For more information on tasks, see "[TK - task feature/concept doc](#)".

#### @workflow

The @workflow decorator indicates a function-esque construct that defines a workflow:

* Workflows specify the flow of data between tasks, and the dependencies between tasks.
* A workflow appears to be a Python function but is actually a DSL that only supports a subset of Python syntax and semantics.
* When deployed to a Flyte cluster the workflow function is "compiled" to construct the directed acyclic graph (DAG) of tasks, defining the order of execution of task pods and the data flow dependencies between them. [TK - what part of the data plane does the compiling?]

For more information on workflows, see "[TK - workflow feature/concept doc](#)".