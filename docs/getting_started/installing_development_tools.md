---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

(getting_started_installing_development_tools)=

# Installing development tools

To create and run workflows in Flyte, you must install Python and Flytekit. We recommend installing conda or another Python virtual environment manager to manage Flytekit and other dependencies, but if you do not, you can install Flytekit with pip.

## Install Python

Python version 3.8x or higher is supported. To install Python, follow the download instructions for your operating system on the [Python downloads site](https://www.python.org/downloads/).

If you already have Python installed, you can use conda or pyenv to install the recommended version.

## (Optional but recommended) Install conda and create a virtual environment

We strongly recommend installing conda with [miniconda](https://docs.conda.io/projects/miniconda/en/latest/) to manage Python versions and virtual environments.

After installing conda, create a virtual environment on the command line:


```{prompt} bash $
conda create -n flyte-example python=3.10 -y
conda activate flyte-example
```

```{note}
You can also use other virtual environment managers, such as [pyenv](https://github.com/pyenv/pyenv) and [venv](https://docs.python.org/3/library/venv.html).
```

## Install Flytekit

If you do not install conda or another virtual environment manager, you will need to install Flytekit.

To install or upgrade Flytekit, run the following command:

```{prompt} bash
pip install -U flytekit
```
