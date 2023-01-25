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

(getting_started_run_and_schedule)=

# Running and Scheduling Workflows

Flyte supports the development and debugging of tasks and workflows in a local
setting, which increases the iteration speed of building out your data-
or machine-learning-driven applications.

Running your workflows locally is great for the initial stages of testing, but
what if you need to make sure that your workflows run as intended on a Flyte
cluster? What if you need to run your workflows on a regular cadence?

In this guide we'll cover how to run and schedule workflows for both development
and production use cases.

```{admonition} Prerequisites
:class: important

This guide assumes that you've completed the previous guides for
{ref}`Initializing a Flyte project <getting_started_creating_flyte_project>` and
{ref}`Packaging and Registering Workflows <getting_started_package_register>`.
Completing 
```

## Create a `FlyteRemote` Object

In the {ref}`Introduction to Flyte <intro_running_flyte_workflows>`, you saw
how to run Flyte workflows with `pyflyte run` in the case that you're working
with standalone scripts.

Once you're working with larger projects where you've registered workflows
to a Flyte cluster, we recommend using the {py:class}`~flytekit.remote.remote.FlyteRemote`
client to run workflows from a Python runtime. First, let's create a `FlyteRemote`
object:

```{code-cell} ipython3
:tags: [remove-output]

from flytekit.remote import FlyteRemote
from flytekit.configuration import Config

remote = FlyteRemote(config=Config.auto())
```

## Running a Workflow

You can run workflows using the `FlyteRemote` {py:meth}`~flytekit.remote.remote.FlyteRemote.execute`
method, where you need to pass in a dictionary of `inputs` that adhere to the
interface defined by the workflow.

`````{tabs}

````{group-tab} Locally Imported

If you have access to the `@workflow`-decorated function in your Python runtime
environment, you can import and execute it directly:

```{code-block} python

from workflows.example import wf

execution = remote.execute(wf, inputs={"name": "Kermit"})
```

````

````{group-tab} Remotely Fetched

Execute a workflow by fetching a `FlyteWorkflow` object from the remote
**FlyteAdmin** service, which essentially contains the metadata representing a
Flyte workflow that exists on a Flyte cluster backend.

```{code-block} python
flyte_wf = remote.fetch_workflow(name="workflows.example.wf")
execution = remote.execute(flyte_wf, inputs={"name": "Kermit"})
```

````

`````

```{note}
You can also launch workflows via `flytectl`, learn more in the {ref}`User Guide <remote_launchplan>`
```

## Running a Task

You can also run individual tasks on a Flyte cluster by using the
`FlyteRemote` {py:meth}`~flytekit.remote.remote.FlyteRemote.execute` method.

`````{tabs}

````{group-tab} Locally Imported

If you have access to the `@task`-decorated function in your Python runtime
environment, you can import and execute it directly:

```{code-block} python

from workflows.example import say_hello

execution = remote.execute(say_hello, inputs={"name": "Kermit"})
```

````

````{group-tab} Remotely Fetched

Execute a task by fetching a `FlyteWorkflow` object from the remote
**FlyteAdmin** service, which essentially contains the metadata representing a
Flyte task that exists on a Flyte cluster backend.

```{code-block} python
flyte_task = remote.fetch_task(name="workflows.example.say_hello")
execution = remote.execute(flyte_task, inputs={"name": "Kermit"})
```

````

`````

```{note}
You can also launch tasks via `flytectl`, learn more in the {ref}`User Guide <remote_task>`
```

## Fetching Inputs and Outputs of an Execution

By default, {py:meth}`FlyteRemote.execute <flytekit.remote.remote.FlyteRemote.execute>`
is non-blocking, but you can also pass in `wait=True` to make it synchronously
wait for the task or workflow to complete.

Print out the Flyte console url corresponding to your execution with:

```{code-block} python
print(f"Execution url: {remote.generate_console_url(execution)}")
```

Synchronize the state of the Flyte execution object with the remote state during
execution with the {py:meth}`~flytekit.remote.remote.FlyteRemote.sync` method:

```{code-block} python
synced_execution = remote.sync(execution)
print(synced_execution.inputs)  # print out the inputs
```

You can also wait for the execution after you've launched it and access the
outputs:

```{code-block} python
completed_execution = remote.wait(execution)
print(completed_execution.outputs)  # print out the outputs
```

## Scheduling a Launch Plan

Finally, you can create a {py:class}`~flytekit.LaunchPlan` that's scheduled
to run at a particular cadence by specifying the `schedule` argument:

```{code-block} python
from flytekit import LaunchPlan, CronSchedule

from workflows.example import wf


launch_plan = LaunchPlan.get_or_create(
    wf,
    name="wf_launchplan",
    # run this launchplan every minute
    schedule=CronSchedule(schedule="*/1 * * * *")
    default_inputs={"name": "Elmo"},
)
```

You can also specify a fixed-rate interval:


```{code-block} python
from datetime import timedelta
from flytekit import FixedRate


launch_plan = LaunchPlan.get_or_create(
    wf,
    name="wf_launchplan",
    schedule=FixedRate(duration=timedelta(minutes=1)),
    default_inputs={"name": "Elmo"},
)
```

### Passing in the Scheduled Kick-off Time

Suppose that your workflow is parameterized to take in a `datetime` argument
that determines how the workflow is executed (e.g. reading in data based on the
current date).

You can specify a `kickoff_time_input_arg` in the schedule so that it
automatically passes the cron schedule kick-off time into the workflow:

```{code-cell} ipython
from datetime import datetime
from flytekit import workflow, LaunchPlan, CronSchedule


@workflow
def process_data_wf(kickoff_time: datetime):
    # read data and process it based on kickoff_time
    ...

process_data_lp = LaunchPlan.get_or_create(
    process_data_wf,
    name="process_data_lp",
    schedule=CronSchedule(
        schedule="*/1 * * * *",
        kickoff_time_input_arg="kickoff_time",
    )
)
```

### Registering Launch Plans

Any of the methods described in the {doc}`package_register` guide will register
a launchplan as long as it's defined in any of the Python modules that you
want to register to a Flyte backend.

### Activating a Schedule

Once you've registered your launch plan, You can use the `FlyteRemote` client or
the `flytectl` CLI to activate the schedule:

:::::{tabs}

::::{group-tab} `FlyteRemote`

:::{code-block}
launchplan_id = remote.fetch_launch_plan(name="process_data_lp").id
remote.client.update_launch_plan(launchplan_id, "ACTIVE")
:::

::::

::::{group-tab} `flytectl`

:::{code-block} bash
flytectl update launchplan -p flyteexamples -d development \
    process_data_lp --version <VERSION> --activate
:::

::::

:::::

### Deactivating a Schedule

Similarly, you can deactivate a launchplan with:

:::::{tabs}

::::{group-tab} `FlyteRemote`

:::{code-block}
launchplan_id = remote.fetch_launch_plan(name="process_data_lp").id
remote.client.update_launch_plan(launchplan_id, "INACTIVE")
:::

::::

::::{group-tab} `flytectl`

:::{code-block} bash
flytectl update launchplan -p flyteexamples -d development \
    process_data_lp --version <VERSION> --archive
:::

::::

:::::

## What's Next?

In this guide, you learned about how to run tasks and workflows using
`FlyteRemote` and how to create a cron schedule to run a launch plan at a
specified time interval. In the next guide, you'll learn how to visualize
tasks using Flyte Decks.
