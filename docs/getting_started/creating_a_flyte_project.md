---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

# Creating a Flyte project

## About Flyte projects

A Flyte project is a directory containing task and workflow code, internal Python source code, configuration files, and other artifacts needed to package up your code so that it can be run on a Flyte cluster.

## Prerequisites

* Follow the steps in {doc}`"Installing development tools" <installing_development_tools>`
* Install git

## Steps

1. Activate your virtual environment
1. Initialize your Flyte project
1. Install additional requirements
1. Version your Flyte project code with git
1. Create a git commit

### Activate your virtual environment

First, activate the virtual environment you will use to manage dependencies for your Flyte project:

```{prompt} bash $
conda activate flyte-example
```

### Initialize your Flyte project

Next, initialize your Flyte project. The [flytekit-python-template GitHub repository](https://github.com/flyteorg/flytekit-python-template) contains Flyte project templates with sample code that you can run as is or modify to suit your needs.

In this example, we will initialize the [simple-example project template](https://github.com/flyteorg/flytekit-python-template/tree/main/simple-example).

```{prompt} bash $
pyflyte init my_project
```

### Install additional requirements

After initializing your Flyte project, you will need to install requirements listed in `requirements.txt`:

```{prompt} bash $
pip install -r requirements.txt
```

### Version your Flyte project code with git

Versioning your Flyte project code allows you to register the workflow it contains to a Flyte cluster and enables workflow versioning.

To version your Flyte project code, initialize a git repository in the Flyte project directory:

```{prompt} bash $
cd my_project
git init
```

### Create a git commit

To ensure you can register your workflow to a Flyte cluster, create at least one git commit:

```{prompt} bash $

git add .
git commit -m "first commit"
```

## Next steps

To learn about the parts of a Flyte project, including tasks and workflows, see {doc} `"Flyte project components" <flyte_project_components>`.

To run the workflow in your Flyte project in a local Python environment or in a local Flyte cluster, see {doc} `"Running a workflow locally" <running_a_workflow_locally>`.

TK - need better language for "both in a local cluster and not" -- what is the term we should use for running locally, but not in a local cluster?
