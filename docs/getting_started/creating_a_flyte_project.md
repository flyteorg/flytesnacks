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
