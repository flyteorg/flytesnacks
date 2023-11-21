---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

(getting_started_creating_a_flyte_project)=

# Creating a Flyte project

## About Flyte projects

A Flyte project is a directory containing workflows, internal Python source code, configuration files, and other artifacts needed to package up your code so that it can be run on a Flyte cluster.

## Prerequisites

* Follow the steps in {ref}`"Installing development tools" <getting_started_installing_development_tools>`
* Install git

## Steps

1. Create a virtual environment with conda (or other tool) to manage dependencies. [TK - if we want people to install flytekit after creating a virtual env, they need to do that after this step]
2. Initialize your Flyte project [TK - slope/intercept example?]
3. Install additional requirements with `pip install -r requirements.txt`.
4. Initialize git repository in your Flyte project directory.
5. Create at least one commit so you can later register the workflow to the local Flyte cluster.

```{note}
TK - benefits of versioning your project.
```

```{note}
For more Flyte project templates, see the [Flyte project template repository](https://github.com/flyteorg/flytekit-python-template/).
```

## Flyte Project components

### Directory structure and configuration files

(getting_started_python_dependencies)=

#### Python dependencies

You can specify additional Python dependencies in your project by updating the
`requirements.txt` file. This gives you the flexibility to use any
pip-installable package that your project may need.

```{note}
We recommend using [pip-compile](https://pip-tools.readthedocs.io/en/latest/) to
manage the requirements of your project.
```

````{dropdown} See requirements.txt

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/requirements.txt
:caption: requirements.txt
```

````

(getting_started_dockerfile)=

#### Dockerfile

The minimal Flyte project ships with a `Dockerfile` that defines the
system requirements for running your tasks and workflows. You can customize this
image to suit your needs:

````{dropdown} See Dockerfile

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/Dockerfile
:language: docker
```

````
```{admonition} ImageSpec
Flyte includes a feature that builds a custom image without having to write a Dockerfile. [Learn more here](https://docs.flyte.org/projects/cookbook/en/latest/auto_examples/customizing_dependencies/image_spec.html#image-spec-example)
```

### Workflow code

In this example, the workflow file [TK - name of file] contains tasks and a workflow, decorated with the `@task` and `@workflow` decorators, respectively.

* The @task and @workflow decorators can be parsed by Python provided that they are used only on functions at the top-level scope of the module.
* Task and workflow function signatures must be type-annotated with Python type hints.
* Tasks and workflows can be invoked like regular Python methods, and even imported and used in other Python modules or scripts.
* Task and workflow functions must be invoked with keyword arguments.

[TK - snippet of example workflow code]

#### @task

The @task decorator indicates a Python function that defines a task.

* A task is a Python function that takes some inputs and produces an output.
* Tasks are assembled into workflows.
* When deployed to a Flyte cluster, each task runs in its own [Kubernetes Pod](https://kubernetes.io/docs/concepts/workloads/pods/), where Flyte orchestrates what task runs at what time in the context of a workflow.

For more information on tasks, see "TK - link to task feature/concept doc".

#### @workflow

The @workflow decorator indicates a function-esque construct that defines a workflow.

* Workflows specify the flow of data between tasks, and the dependencies between tasks.
* A workflow appears to be a Python function but is actually a DSL that only supports a subset of Python syntax and semantics.
* When deployed to a Flyte cluster the workflow function is "compiled" to construct the directed acyclic graph (DAG) of tasks, defining the order of execution of task pods and the data flow dependencies between them. [TK - what part of the data plane does the compiling?]

For more information on workflows, see "TK - link to workflow feature/concept doc".
