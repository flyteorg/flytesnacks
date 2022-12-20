---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(getting_started_init_flyte_project)=

# Initializing a Flyte Project

So far we've been dealing with fairly simple workflows composed of a handful of
tasks, all of which can fit into a single Python script. In this guide, you'll
learn how to organize a Flyte project so that it can scale to a larger codebase.

```{admonition} Prerequisites
:class: important

Install `flytekit` and `flytectl` according to the
[introduction guide](getting_started_installation) instructions.
```

`pyflyte`, the CLI tool that ships with `flytekit`, comes with an `init` command
that you can use to quickly initialize a Flyte project according to the
recommended file structure.

```{prompt} bash $
pyflyte init my_project
cd my_project
```

## Project Structure

If you examine `my_project`, you'll see the following file structure:

```{code-block} bash
.
├── Dockerfile        # Docker image
├── LICENSE
├── README.md
├── docker_build.sh   # Docker build helper script
├── requirements.txt  # Python dependencies
└── workflows
    ├── __init__.py
    ├── example.py    # Example Flyte workflows
    └── helpers.py    # Helper functions
```

In the rest of this guide we'll orient you to all the important pieces of the
minimal Flyte project template.

## Workflow Source Code

The `workflows/example.py` module contains a simple set of tasks and workflows
that you can use to make sure that everything's working as expected:

```{prompt} bash $
python workflows/example.py
```

````{dropdown} See Workflow

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/workflows/example.py
:language: python
```

````

````{div} shadow p-3 mb-8 rounded
**Expected output**

```{code-block}
Running wf() DefaultNamedTupleOutput(o0='hello passengers!', o1=17)
```

````

The `workflows/helpers.py` module demonstrates how you can include additional
pure Python functions/classes in your project, which you can then import into
your workflow modules.

````{div} shadow p-3 mb-8 rounded

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/workflows/helpers.py
:language: python
:caption: workflows/helpers.py
```

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/workflows/example.py
:caption: workflows/example.py
:language: python
:lines: 1-7,19-22
:emphasize-lines: 6,11
```

````

## Python Dependencies

You can specify additional Python dependencies in your project by updating the
`requirements.txt` file. This gives you the flexibility to use any
pip-installable package that your project may need.

```{note}
We recommend using [pip-compile](https://pip-tools.readthedocs.io/en/latest/) to
manage the requirements of your project.
```


## Dockerfile

The minimal Flyte project ships with a `Dockerfile` script that defines the
minimum system requirements for running your tasks and workflows. You can
customize this image to suit your needs:

````{dropdown} See Dockerfile

```{rli} https://raw.githubusercontent.com/flyteorg/flytekit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/Dockerfile
:language: docker
```

````

The default template also includes a `docker_build.sh` script  that you can use
to build a Docker image according to the recommended practice:

```{prompt} bash $
./docker_build.sh
```

By default, the `docker_build.sh` script:

- Uses the `PROJECT_NAME` specified in the `pyflyte init` command.
- Will not use any remote registry.
- Uses the git sha to version your tasks and workflows.

Override any of these values with the following flags:

```{prompt} bash $
./docker_build.sh -p <PROJECT_NAME> -r <REGISTRY> -v <VERSION>
```

For example, if you want to push your Docker image to Github's image registry
you can specify the `-r ghcr.io` flag.

```{note}
You can create your own way of building your Docker containers, the
`docker_build.sh` is for convenience.
```

## What's Next?

In summary, this guide took you through the recommended way of initializing and
structuring a larger Flyte codebase. In the next guide, we'll walk through how
to package register your tasks and workflows so that they can be executed on
a Flyte cluster.
