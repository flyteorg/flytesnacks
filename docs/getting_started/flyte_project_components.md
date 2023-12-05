---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

# Flyte project components

A Flyte project is a directory containing task and workflow code, internal Python source code, configuration files, and other artifacts needed to package up your code so that it can be run on a Flyte cluster.

## Directory structure

If you examine the project you created with `pyflyte init` in {doc}`"Creating a Flyte project <creating_a_flyte_project>"`, you'll see the following directory structure:

```{code-block} bash
my_project
├── Dockerfile        # Docker image
├── LICENSE
├── README.md
├── docker_build.sh   # Docker build helper script
├── requirements.txt  # Python dependencies
└── workflows
    ├── __init__.py
    └── example.py    # Example Flyte workflows
```

## Configuration files

Flyte projects contain a `Dockerfile` and `requirements.txt` file that you can modify to suit the needs of your project.

(getting_started_python_dependencies)=

### `requirements.txt` Python dependencies

You can specify pip-installable Python dependencies in your project by adding them to the
`requirements.txt` file.

```{note}
We recommend using [pip-compile](https://pip-tools.readthedocs.io/en/latest/) to
manage your project's Python requirements.
```

````{dropdown} See requirements.txt

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/requirements.txt
:caption: requirements.txt
```

````

(getting_started_dockerfile)=

### Dockerfile

Flyte projects contain a `Dockerfile` that defines the system requirements for running the tasks and workflows in the project that you can customize as needed.

````{dropdown} See Dockerfile

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/Dockerfile
:language: docker
```

````
```{note}
Flyte includes ImageSpec, a feature that builds a custom image without having to write a Dockerfile. To learn more, see the [ImageSpec documentation](https://docs.flyte.org/projects/cookbook/en/latest/auto_examples/customizing_dependencies/image_spec.html#image-spec-example)
```

(getting_started_workflow_code)=

## Workflow code

By default, Flyte projects contain a `workflows` directory, inside of which is a Python file that holds the workflow code for the application.

The workflow code contains one or more task and workflow functions, decorated with the `@task` and `@workflow` decorators, respectively.

* The @task and @workflow decorators can be parsed by Python provided that they are used only on functions at the top-level scope of the module.
* Task and workflow function signatures must be type-annotated with Python type hints.
* Tasks and workflows can be invoked like regular Python methods, and even imported and used in other Python modules or scripts.
* Task and workflow functions must be invoked with keyword arguments.

```{note}
The workflow directory also contains an `__init__.py` file to indicate that the workflow code is part of a Python package. For more information, see the [Python documentation](https://docs.python.org/3/reference/import.html#regular-packages).
```

### @task decorator

The @task decorator indicates a Python function that defines a task.

* A task is a Python function that takes some inputs and produces an output.
* Tasks are assembled into workflows.
* When deployed to a Flyte cluster, each task runs in its own [Kubernetes Pod](https://kubernetes.io/docs/concepts/workloads/pods/), where Flyte orchestrates what task runs at what time in the context of a workflow.

### @workflow decorator

The @workflow decorator indicates a function-esque construct that defines a workflow.

* Workflows specify the flow of data between tasks, and the dependencies between tasks.
* A workflow appears to be a Python function but is actually a [domain-specific language (DSL)](https://en.wikipedia.org/wiki/Domain-specific_language) that only supports a subset of Python syntax and semantics.
* When deployed to a Flyte cluster, the workflow function is "compiled" to construct the directed acyclic graph (DAG) of tasks, defining the order of execution of task pods and the data flow dependencies between them.
