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

A Flyte project is a directory containing task and workflow code, internal Python source code, configuration files, and other artifacts needed to package up your code so that it can be run on a Flyte cluster.

## Prerequisites

* Follow the steps in {ref}`"Installing development tools" <getting_started_installing_development_tools>`
* Install git

## Steps

1. Create a virtual environment
2. Initialize your Flyte project
3. Install additional requirements
4. Initialize a git repository
5. Create a git commit

### Create a virtual environment

To manage dependencies, create a virtual environment with conda (or other tool) for your Flyte project.
[TK - if we want people to install flytekit after creating a virtual env, they need to do that after this step]

```{prompt} bash $
TK - conda example
```

### Initialize your Flyte project

Next, you will need to initialize your Flyte project. The [flytekit-python-template GitHub repository](https://github.com/flyteorg/flytekit-python-template) contains Flyte project templates with sample code that you can run as is or modify to suit your needs. In this example, we will initialize the [simple-example project template](https://github.com/flyteorg/flytekit-python-template/tree/main/simple-example).

```{prompt} bash $
TK - pyflyte init example
```

### Install additional requirements

After initializing your Flyte project, you will need to install requirements listed in `requirements.txt`:

```{prompt} bash $
pip install -r requirements.txt
```

### Initialize a git repository

TK - benefits of versioning Flyte project code: get versioned workflows and can register the workflow to a Flyte cluster

To version your code, initialize a git repository in the Flyte project directory:

```{prompt} bash $
git init .
```

### Create a git commit

To ensure you can register the workflow to a Flyte cluster, create at least one git commit:

```{prompt} bash $

git add .
git commit -m "first commit"
```
