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

* Install Python
* Install Flytekit

## Steps

1. Create the "Hello, world" example Python file. [TK]
2. Run the workflow with `pyflyte run`

## The @task and @workflow decorators

In this example, the workflow file [TK - name of file] contains tasks and a workflow, decorated with the `@task` and `@workflow` decorators, respectively. You can invoke tasks and workflows like regular Python methods, and even import and use them in other Python modules or scripts.

### @task

The @task decorator indicates functions that define tasks:

* A task is a Python function that takes some inputs and produces an output.
* When deployed to a Flyte cluster, each task runs in its own Kubernetes pod.
* Tasks are assembled into workflows.

For more information on tasks, see "[TK - task feature/concept doc](#)".

### @workflow

The @workflow decorator indicates a function-esque construct that defines a workflow

* Workflows specify the flow of data between tasks, and the dependencies between tasks.
* A workflow appears to be a Python function but is actually a DSL that only supports a subset of Python syntax and semantics.
* When deployed to a Flyte cluster the workflow function is "compiled" to construct the directed acyclic graph (DAG) of tasks, defining the order of execution of task pods and the data flow dependencies between them. TK - what part of the data plane does the compiling?

For more information on workflows, see "TK - link to workflow concept / feature doc".

## Next steps

To create a Flyte Project and run the workflow in a local Flyte cluster, see "[Getting started with Flyte development](#)".
