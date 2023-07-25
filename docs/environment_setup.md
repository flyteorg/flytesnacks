(env_setup)=

# Environment Setup

## Prerequisites

- Make sure you have [docker](https://docs.docker.com/get-docker/) and [git](https://git-scm.com/) installed.
- Install {doc}`flytectl <flytectl:index>`, the commandline interface for flyte.

## Repo Setup

Clone the `flytesnacks` repo and install its dependencies, which includes
{doc}`flytekit <flytekit:index>`.

:::{tip}
**Recommended**: Create a new python virtual environment to make sure it doesn't interfere with your
development environment, e.g. with:

```{prompt} bash
python -m venv ~/venvs/flytesnacks-basics
source ~/venvs/flytesnacks-basics/bin/activate
```
:::

The `examples` directory contains all of the examples in the
{ref}`User Guides <userguide>`, {ref}`Tutorials <tutorials>`, and
{ref}`Integrations <integrations>` sections.

In this setup guide, let's run the `examples/basics` project.

```{prompt} bash
git clone https://github.com/flyteorg/flytesnacks

# or if your SSH key is registered on GitHub:
git clone git@github.com:flyteorg/flytesnacks.git

# or if you use the `gh` tool:
gh repo clone flyteorg/flytesnacks
cd flytesnacks/examples/basics
pip install -r requirements.txt
```

To make sure everything is working in your virtual environment, run `hello_world.py` locally:

```{prompt} bash
python basics/hello_world.py
```

Expected output:

```{prompt}
Running my_wf() hello world
```

## Create a Local Demo Flyte Cluster

```{important}
Make sure the Docker daemon is running before starting the demo cluster.
```

Use `flytectl` to start a demo Flyte cluster:

```{prompt} bash
flytectl demo start
```

## Running Workflows

Now you can run all of the example workflows locally using the default Docker image bundled with `flytekit`:

```{prompt} bash
pyflyte run basics/hello_world.py my_wf
```

:::{note}
The first two arguments to `pyflyte run` have the form of 
`path/to/script.py <workflow_name>`, where `<workflow_name>` is the function 
decorated with `@workflow` that you want to run.
:::

To run the workflow on the demo Flyte cluster, all you need to do is supply the `--remote` flag:

```{prompt} bash
pyflyte run --remote basics/hello_world.py my_wf
```

You should see an output that looks like:

```{prompt}
Go to https://<flyte_admin_url>/console/projects/flytesnacks/domains/development/executions/<execution_name> to see execution in the console.
```

You can visit this url to inspect the execution as it runs:

:::{figure} https://raw.githubusercontent.com/flyteorg/static-resources/main/common/first_run_console.gif
:alt: A quick visual tour for launching your first Workflow.
:::

Finally, let's run a workflow that takes some inputs, for example the `basic_workflow.py` example:

```{prompt} bash
pyflyte run --remote basics/basic_workflow.py my_wf --a 5 --b hello
```

:::{note}
We're passing in the workflow inputs as additional options to `pyflyte run`, in the above example the
inputs are `--a 5` and `--b hello`. For snake-case argument names like `arg_name`, you can provide the
option as `--arg-name`.
:::

## Visualizing Workflows

Workflows can be visualized as DAGs in the UI. You can also visualize workflows
from your terminal that will be displayed in your default web browser. This
visualization uses the service at graph.flyte.org to render Graphviz diagrams,
and hence shares your DAG (but not your data or code) with an outside party 
(security hint 🔐).

To view workflow on the browser:

```{prompt} bash $
flytectl get workflows \
    --project flytesnacks \
    --domain development \
    --version <version> \
    -o doturl \
    basics.basic_workflow.my_wf
```

To view workflow as a `strict digraph` on the command line:

```{prompt} bash $
flytectl get workflows \
    --project flytesnacks \
    --domain development \
    --version <version> \
    -o dot \
    basics.basic_workflow.my_wf
```

Replace `<version>` with the base64-encoded version shown in the console UI,
that looks something like `BLrGKJaYsW2ME1PaoirK1g==`.

:::{tip}

Running most of the examples in the **User Guide** only requires the default
Docker image that ships with Flyte. Many examples in the {ref}`tutorials` and
{ref}`integrations` section depend on additional libraries such as `sklearn`,
`pytorch`, or `tensorflow`, which will not work with the default docker image 
used by `pyflyte run`.

These examples will explicitly show you which images to use for running these
examples by passing in the docker image you want to use with the `--image`
option in `pyflyte run`.
:::

🎉 Congrats! Now you can run all the examples in the {ref}`userguide` 🎉

## What's Next?

Try out the examples in {doc}`Flyte Basics <auto_examples/basics/index>` section.
