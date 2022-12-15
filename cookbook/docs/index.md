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

(getting_started_index)=

# Introduction to Flyte

[Flytesnacks Tags](_tags/tagsindex)

Flyte is a workflow orchestrator that seamlessly unifies ETL/ELT,
machine learning, and analytics stacks for building robust and reliable
applications.

This quickstart guide provides an overview of how to get Flyte up and running
on your local machine.

## Installation

```{admonition} Prerequisites
:class: important

[Install Docker](https://docs.docker.com/get-docker/) and ensure that the Docker
daemon is running.
```

First install [flytekit](https://pypi.org/project/flytekit/), Flyte's Python SDK.

```{prompt} bash $
pip install flytekit
```

Then install [flytectl](https://docs.flyte.org/projects/flytectl/en/latest/),
which the command-line interface for interacting with a Flyte backend.

````{tabbed} OSX

```{prompt} bash $
brew install flyteorg/homebrew-tap/flytectl
```

````

````{tabbed} Other Operating systems

```{prompt} bash $
curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin
```

````

## Creating a Workflow

The first workflow we'll create is a simple model training workflow that consists
of three steps:

1. 🍷 Gets the classic [wine dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-recognition-dataset)
   using [sklearn](https://scikit-learn.org/stable/).
2. 📊 Processes the data that simplifies the 3-class prediction problem into a
   binary classification problem by consolidating class labels `1` and `2` into
   a single class.
3. 🤖 Trains a `LogisticRegression` model to learn a binary classifier.

First, we'll define three tasks for each of these steps. Create a file called
`example.py` and copy the following code into it.

```{code-cell} python
:tags: [remove-output]

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression

from flytekit import task, workflow
from flytekit.types.pickle import FlytePickle


@task
def get_data() -> pd.DataFrame:
    """Get the wine dataset."""
    return load_wine(as_frame=True).frame

@task
def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Simplify the task from a 3-class to a binary classification problem."""
    return data.assign(target=lambda x: x["target"].where(x["target"] == 0, 1))

@task
def train_model(data: pd.DataFrame, hyperparameters: dict) -> LogisticRegression:
    """Train a model on the wine dataset."""
    features = data.drop("target", axis="columns")
    target = data["target"]
    return LogisticRegression(**hyperparameters).fit(features, target)
```

As we can see in the code snippet above, we defined three tasks as Python
functions: `get_data`, `process_data`, and `train_model`.

In Flyte, a **task** is the most basic unit of compute and serves as the building
block 🧱 for more complex applications. It's a function that takes some inputs and
(optionally) produces an output. We can use these tasks to define a simple model
training workflow:

```{code-cell} python
@workflow
def training_workflow(hyperparameters: dict) -> FlytePickle:
    """Put all of the steps together into a single workflow."""
    data = get_data()
    processed_data = process_data(data=data)
    return train_model(
        data=processed_data,
        hyperparameters=hyperparameters,
    )
```

A **workflow** is also defined as a Python function, and it specifies the flow
of data between tasks and, more generally, the dependencies between tasks 🔀.

::::{dropdown} {fa}`info-circle` The code above looks like Python, but what do `@task` and `@workflow` do exactly?
:title: text-muted
:animate: fade-in-slide-down

Flyte `@task` and `@workflow` decorators are designed to work seamlessly with
your code-base, provided that the *decorated function is at the top-level scope
of the module*.

This means that you can invoke tasks and workflows as regular Python methods and
even import and use them in other Python modules or scripts.

:::{note}
A {func}`~flytekit.task` is a pure Python function, while a {func}`~flytekit.workflow`
is actually a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) that
only supports a subset of Python's semantics. Some key things to learn here are:

- In workflows, you can't use non-deterministic operations like `rand.random`,
  `time.now()`, etc.
- Within workflows, the outputs of tasks are promises under the hood, so you
  can't access and operate on them like typical Python function outputs.
  *You can only pass promises into other tasks/workflows.*
- Tasks can only be invoked with keyword arguments, not positional arguments.

You can read more about tasks {doc}`here <auto/core/flyte_basics/task>` and workflows
{doc}`here <auto/core/flyte_basics/basic_workflow>`.
:::

::::

## Running Flyte Workflows

You can run the workflow in ``example.py`` on a local Python environment or a
Flyte cluster.

### Local Execution

You can run your workflow using `pyflyte`, the CLI that ships with `flytekit`.

```{prompt} bash $
pyflyte run example.py training_workflow --hyperparameters '{"C": 0.1, "max_iter": 3000}'
```

:::::{dropdown} {fa}`info-circle` Why use `pyflyte run` rather than `python example.py`?
:title: text-muted
:animate: fade-in-slide-down

`pyflyte run` enables you to execute a specific workflow using the syntax
`pyflyte run <path/to/script.py> <workflow_or_task_function_name>`.

Keyword arguments can be supplied to ``pyflyte run`` by passing in options in
the format ``--kwarg value``, and in the case of ``snake_case_arg`` argument
names, you can pass in options in the form of ``--snake-case-arg value``.

::::{note}
If you want to run a workflow with `python example.py`, you would have to write
a `main` module conditional at the end of the script to actually run the
workflow:

:::{code-block} python
if __name__ == "__main__":
    training_workflow(hyperparameters={"C": 0.1, "max_iter": 3000})
:::

This becomes even more verbose if you want to pass in arguments:

:::{code-block} python
if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--hyperparameters", type=json.loads)
    ...  # add the other options

    args = parser.parse_args()
    training_workflow(hyperparameters=args.hyperparameters)
:::

::::

:::::


### Flyte Cluster Execution

To run your Flyte workflows on an actual Flyte cluster, spin up a local demo
cluster:

```{prompt} bash $
flytectl demo start
```

````{div} shadow p-3 mb-8 rounded
**Expected Output:**

```{code-block}
👨‍💻 Flyte is ready! Flyte UI is available at http://localhost:30080/console 🚀 🚀 🎉
Add KUBECONFIG and FLYTECTL_CONFIG to your environment variable
export KUBECONFIG=$KUBECONFIG:/Users/<username>/.kube/config:/Users/<username>/.flyte/k3s/k3s.yaml
export FLYTECTL_CONFIG=/Users/<username>/.flyte/config-sandbox.yaml
```

```{important}
Make sure to export the `KUBECONFIG` and `FLYTECTL_CONFIG` environment variables
in your shell.
```
````

Run the workflow on the Flyte cluster with `pyflyte run` using the `--remote`
flag:

```{prompt} bash $
pyflyte run --remote example.py training_workflow --hyperparameters '{"C": 0.1, "max_iter": 3000}'
```

````{div} shadow p-3 mb-8 rounded

**Expected Output:** A URL to the workflow execution on your demo Flyte cluster:

```{code-block}
Go to http://localhost:30080/console/projects/flytesnacks/domains/development/executions/<execution_name> to see execution in the console.
```

Where ``<execution_name>`` is a unique identifier for the workflow execution.

````

Unlike the previous ``pyflyte run`` invocation, passing the ``--remote`` flag
will trigger the execution on the configured backend.


## Inspect the Results

Navigate to the URL produced as the result of running `pyflyte run`. This will
take you to FlyteConsole, the web UI used to manage Flyte entities such as tasks,
workflows, and executions.

![getting started console](https://github.com/flyteorg/static-resources/raw/main/flytesnacks/getting_started/getting_started_console.gif)


```{note}
There are a few features about FlyteConsole worth pointing out in the GIF above:

- The default execution view shows the list of tasks executing in sequential order.
- The right-hand panel shows metadata about the task execution, including logs, inputs, outputs, and task metadata.
- The **Graph** view shows the execution graph of the workflow, providing visual information about the topology
  of the graph and the state of each node as the workflow progresses.
- On completion, you can inspect the outputs of each task, and ultimately, the overarching workflow.
```

## Recap

🎉  **Congratulations! In this introductory guide, you:**

1. 📜 Created a Flyte script, which trains a binary classification model.
2. 🚀 Created a demo Flyte cluster on your local system.
3. 👟 Ran a workflow locally and on a demo Flyte cluster.


## What's Next?

Follow the rest of the guides in the **Getting Started** section to get a
better understanding of the key constructs that make Flyte a such powerful
orchestration tool 💪.


```{toctree}
:maxdepth: 1
:hidden:

|plane| Getting Started <self>
|book-reader| User Guide <userguide>
|chalkboard| Tutorials <tutorials>
|project-diagram| Concepts <https://docs.flyte.org/en/latest/concepts/basics.html>
|rocket| Deployment <https://docs.flyte.org/en/latest/deployment/index.html>
|book| API Reference <https://docs.flyte.org/en/latest/reference/index.html>
|hands-helping| Community <https://docs.flyte.org/en/latest/community/index.html>
```

```{toctree}
:maxdepth: -1
:caption: Getting Started
:hidden:

self
```

```{toctree}
:maxdepth: -1
:caption: User Guide
:hidden:

User Guide <userguide>
Environment Setup <userguide_setup>
Basics <auto/core/flyte_basics/index>
Control Flow <auto/core/control_flow/index>
Type System <auto/core/type_system/index>
Testing <auto/testing/index>
Containerization <auto/core/containerization/index>
Remote Access <auto/remote_access/index>
Production Config <auto/deployment/index>
Scheduling Workflows <auto/core/scheduled_workflows/index>
Extending Flyte <auto/core/extend_flyte/index>
Building Large Apps <auto/larger_apps/index>
Example Contribution Guide <contribute>
```

```{toctree}
:maxdepth: -1
:caption: Tutorials
:hidden:

Tutorials <tutorials>
ml_training
feature_engineering
bioinformatics_examples
flyte_lab
```

```{toctree}
:maxdepth: -1
:caption: Integrations
:hidden:

Integrations <integrations>
auto/integrations/flytekit_plugins/sql/index
auto/integrations/flytekit_plugins/greatexpectations/index
auto/integrations/flytekit_plugins/papermilltasks/index
auto/integrations/flytekit_plugins/pandera_examples/index
auto/integrations/flytekit_plugins/modin_examples/index
auto/integrations/flytekit_plugins/dolt/index
auto/integrations/flytekit_plugins/whylogs_examples/index
auto/integrations/flytekit_plugins/onnx_examples/index
auto/integrations/kubernetes/pod/index
auto/integrations/kubernetes/k8s_spark/index
auto/integrations/kubernetes/kfpytorch/index
auto/integrations/kubernetes/kftensorflow/index
auto/integrations/kubernetes/kfmpi/index
auto/integrations/kubernetes/ray_example/index
auto/integrations/aws/sagemaker_training/index
auto/integrations/aws/sagemaker_pytorch/index
auto/integrations/aws/athena/index
auto/integrations/aws/batch/index
auto/integrations/external_services/hive/index
auto/integrations/external_services/snowflake/index
auto/integrations/gcp/bigquery/index
auto/integrations/external_services/airflow/index
```
