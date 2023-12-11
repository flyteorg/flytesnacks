---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

# Creating a Flyte project

## About Flyte projects

A Flyte project is a directory containing task and workflow code, internal Python source code, configuration files, and other artifacts structured according to software engineering best practices that enables you to package up your code so that it can be registered to a Flyte cluster.

## Prerequisites

* Follow the steps in {doc}`"Installing development tools" <installing_development_tools>`
* Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Steps

1. Activate your virtual environment
1. Initialize your Flyte project
1. Install additional requirements
1. (Optional) Version your Flyte project with git

### Activate your virtual environment

First, activate the virtual environment you will use to manage dependencies for your Flyte project:

```{prompt} bash $
conda activate flyte-example
```

### Initialize your Flyte project

Next, initialize your Flyte project. The [flytekit-python-template GitHub repository](https://github.com/flyteorg/flytekit-python-template) contains Flyte project templates with sample code that you can run as is or modify to suit your needs.

In this example, we will initialize the [basic-example-imagespec project template](https://github.com/flyteorg/flytekit-python-template/tree/main/basic-example-imagespec).

```{prompt} bash $
pyflyte init my_project
```

### Install additional requirements

After initializing your Flyte project, you will need to install requirements listed in `requirements.txt`:

```{prompt} bash $
pip install -r requirements.txt
```

### (Optional) Version your Flyte project with git

We highly recommend putting your Flyte project code under version control. To do so, initialize a git repository in the Flyte project directory:

```{prompt} bash $
cd my_project
git init
```

```{note}
If you are using a Dockerfile instead of ImageSpec, you will need to initialize a git repository and create at least one commit, since the commit hash is used to tag the image when it is built.
```

### Run your workflow in a local Python environment

To check that your Flyte project was set up correctly, run the workflow in a local Python environment:

```{prompt} bash $
cd my_project/workflows
pyflyte run example.py wf
```

:::{note}
While you can run the example file like a Python script with `python example.py`, we recommend using `pyflyte run` instead. To run the file like a Python script, you need to include the `main` module conditional at the end of the script:
```python
if __name__ == "__main__":
    print(f"Running wf() { wf(name='passengers') }")
```

Your code would become even more verbose if you wanted to pass arguments to the workflow:
```python
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--name", type=str)

    args = parser.parse_args()
    print(f"Running wf() {wf(name=args.name) }")
```
:::

## Next steps

To learn about the parts of a Flyte project, including tasks and workflows, see {doc}`"Flyte project components" <flyte_project_components>`.

To run the workflow in your Flyte project in a local Flyte cluster, see the {ref}`"Running a workflow in a local cluster" <getting_started_running_workflow_local_cluster>` section of {doc}`"Running a workflow locally" <running_a_workflow_locally>`.
