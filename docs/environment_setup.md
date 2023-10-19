(env_setup)=

# Environment Setup

## Prerequisites

- Make sure you have [docker](https://docs.docker.com/get-docker/) and [git](https://git-scm.com/) installed.
- Install {doc}`flytectl <flytectl:index>`, the commandline interface for Flyte.

## Repo setup

As we intend to execute the code locally, duplicate this code block into `hello_world.py`.

```python
from flytekit import task, workflow

@task
def say_hello() -> str:
    return "Hello, World!"

@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res

if __name__ == "__main__":
    print(f"Running hello_world_wf() {hello_world_wf()}")
```

To install `flytekit`, run the following command:

```
pip install flytekit
```

:::{tip}
**Recommended**: Create a new python virtual environment to make sure it doesn't interfere with your
development environment. You can do this by running the following commands in your terminal:

```{prompt} bash
python -m venv ~/venvs/flyte-examples
source ~/venvs/flyte-examples/bin/activate
```

:::

To make sure everything is working in your virtual environment, run `hello_world.py` locally:

```{prompt} bash
python hello_world.py
```

Expected output:

```{prompt}
Running hello_world_wf() Hello, World!
```

## Create a local demo Flyte cluster

```{important}
Make sure the Docker daemon is running before starting the demo cluster.
```

Use `flytectl` to start a demo Flyte cluster:

```{prompt} bash
flytectl demo start
```

## Running workflows

Now you can run the example workflow locally using the default Docker image bundled with `flytekit`:

```{prompt} bash
pyflyte run hello_world.py hello_world_wf
```

:::{note}
The initial arguments of `pyflyte run` take the form of
`path/to/script.py <task_or_workflow_name>`, where `<task_or_workflow_name>`
refers to the function decorated with `@task` or `@workflow` that you wish to run.
:::

To run the workflow on the demo Flyte cluster, all you need to do is supply the `--remote` flag:

```
pyflyte run --remote hello_world.py hello_world_wf
```

You can also run the code directly from a remote source:

```
pyflyte run --remote \
    https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/basics/basics/hello_world.py \
    hello_world_wf
```

You should see an output that looks like:

```{prompt}
Go to https://<flyte_admin_url>/console/projects/flytesnacks/domains/development/executions/<execution_name> to see execution in the console.
```

You can visit this URL to inspect the execution as it runs:

:::{figure} https://raw.githubusercontent.com/flyteorg/static-resources/main/common/first_run_console.gif
:alt: A quick visual tour for launching your first Workflow.
:::

Finally, run a workflow that takes some inputs, for example the `workflow.py` example:

```{prompt} bash
pyflyte run --remote \
    https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/basics/basics/workflow.py \
    simple_wf --x '[-3,0,3]' --y '[7,4,-2]'
```

:::{note}
We're passing in the workflow inputs as additional options to `pyflyte run`. In the above example, the
inputs are `--x '[-3,0,3]'` and `--y '[7,4,-2]'`. For snake-case argument names like `arg_name`, you can provide the
option as `--arg-name`.
:::

## Visualizing workflows

Workflows can be visualized as DAGs on the UI.
However, you can visualize workflows on the browser and in the terminal by _just_ using your terminal.

To view workflow on the browser:

```{prompt} bash $
flytectl get workflows \
    --project flytesnacks \
    --domain development \
    --version <version> \
    -o doturl \
    basics.workflow.simple_wf
```

To view workflow as a `strict digraph` on the command line:

```{prompt} bash $
flytectl get workflows \
    --project flytesnacks \
    --domain development \
    --version <version> \
    -o dot \
    basics.workflow.simple_wf
```

Replace `<version>` with the version obtained from the console UI,
which might resemble something like `BLrGKJaYsW2ME1PaoirK1g==`.

:::{tip}
Running most of the examples in the **User Guide** only requires the default Docker image that ships with Flyte.
Many examples in the {ref}`tutorials` and {ref}`integrations` section depend on additional libraries such as
`sklearn`, `pytorch` or `tensorflow`, which will not work with the default docker image used by `pyflyte run`.

These examples will explicitly show you which images to use for running these examples by passing in the Docker
image you want to use with the `--image` option in `pyflyte run`.
:::

🎉 Congrats! Now you can run all the examples in the {ref}`userguide` 🎉

## Demo cluster configuration

Depending on the intensity of your workflows, you may encounter errors such as OOM (Out of Memory) errors or find pods with the status: OOMKilled.
It is critical to understand that the demo cluster is not setup to immediately accept any and all workflow requirements, and some resource requests may be ignored depending on the cluster's limits.

:::{tip}
**Keep in mind that for production deployments, you should put more thought into these configurations - rather than just setting large numbers.**

As an example of what settings are available to you, you can alter the demo cluster's memory and cpu limit configurations by following a few simple steps:

1. Create the file `cra.yaml` with the following text:

```
attributes:
    projectQuotaCpu: "1000"
    projectQuotaMemory: 5Ti
project: flytesnacks
domain: development
```

2. Create the file `tra.yaml` with the following text:

```
defaults:
    cpu: "2"
    memory: 1Gi
limits:
    cpu: "1000"
    memory: 5Ti
project: flytesnacks
domain: development
```

3. Apply the two configuration files via:

```
$ flytectl update task-resource-attribute --attrFile tra.yaml --config ~/.flyte/config-sandbox.yaml
$ flytectl update cluster-resource-attribute --attrFile cra.yaml --config ~/.flyte/config-sandbox.yaml
```

4. Confirm the configuration via:

```
$ flytectl get task-resource-attribute --config ~/.flyte/config-sandbox.yaml -p flytesnacks -d development
{"project":"flytesnacks","domain":"development","defaults":{"cpu":"2","memory":"1Gi"},"limits":{"cpu":"1000","memory":"5Ti"}}

$ flytectl get cluster-resource-attribute --config ~/.flyte/config-sandbox.yaml -p flytesnacks -d development
{"project":"flytesnacks","domain":"development","attributes":{"projectQuotaCpu":"1000","projectQuotaMemory":"5Ti"}}
```

And that's it! You have now altered your flyte demo cluster to enable significantly more intensive workloads.

For more information see: :ref:`deployment/configuration/general:Configuring Custom K8s Resources` 

### Demo cluster envd ImageSpec preparation

If you find yourself using tasks dependant on `ImageSpec` containers that are built with `envd` with the `demo` or `sandbox` clusters,
before you submit your workflow you will need to inform `envd` how to push the images it builds to the cluster. This can
be done via:

```
envd context create --name flyte-sandbox --builder tcp --builder-address localhost:30003 --use
```
You will also need to update your `ImageSpec` instances to set `registry="localhost:30000"`


## What's next?

Try out the examples in the {doc}`Basics <auto_examples/basics/index>` section.
