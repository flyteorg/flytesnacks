(plugins-dask-k8s)=

# Dask

```{eval-rst}
.. tags:: Dask, Integration, DistributedComputing, Data, Advanced
```

Flyte can natively execute [Dask](https://www.dask.org/) jobs on a Kubernetes Cluster,
effortlessly managing the lifecycle of a virtual Dask cluster.
This functionality is achieved by leveraging the open-sourced
[Dask Kubernetes Operator](https://kubernetes.dask.org/en/latest/operator.html),
and no additional sign-ups for services are required.
The process is akin to running an ephemeral Dask cluster,
which is created specifically for the Flyte task and subsequently torn down upon completion.

In the Flyte Kubernetes environment, the cost is amortized due to faster pod creation compared to machines.
However, the performance may be affected by the penalty of downloading Docker images.
Additionally, it's essential to keep in mind that starting a pod is not as swift as running a process.

Flytekit enables writing Dask code natively as a task,
with the `Dask()` config automatically configuring the Dask cluster.
The example provided in this section offers a hands-on tutorial for writing Dask Flyte tasks.

## Why use Kubernetes Dask?

Managing Python dependencies can be challenging, but Flyte simplifies the process
by enabling easy versioning and management of dependencies through containers.
The Kubernetes Dask plugin extends the benefits of containerization to Dask without
requiring the management of specialized Dask clusters.

Pros:

1. Simple to get started, providing complete isolation between workloads.
2. Each job runs in isolation with its own virtual cluster, eliminating the complexities of dependency management.
3. Flyte takes care of all the management tasks.

Cons:

1. Short-running, bursty jobs may not be the best fit due to container overhead.
2. Interactive Dask capabilities are not available with Flyte Kubernetes Dask;
   instead, it is better suited for running adhoc and scheduled jobs.

## Install the plugin

Install `flytekitplugins-dask` using `pip` in your environment.

```
pip install flytekitplugins-dask
```

:::{note}
To enable Flyte to build the Docker image for you using `ImageSpec`, install `flytekitplugins-envd`.
:::

## Implementation details

### Local execution

When executing the Dask task on your local machine,
it will utilize a local [distributed client](https://distributed.dask.org/en/stable/client.html).
If you intend to link to a remote cluster during local development, simply define the `DASK_SCHEDULER_ADDRESS`
environment variable with the URL of the remote scheduler.
The `Client()` will then automatically connect to the cluster.

### Remote execution

#### Step 1: Deploy Dask plugin in the Flyte backend

Flyte Dask utilizes the [Dask Kubernetes operator](https://kubernetes.dask.org/en/latest/operator.html)
in conjunction with a custom-built
[Flyte Dask plugin](https://pkg.go.dev/github.com/flyteorg/flyteplugins@v1.0.28/go/tasks/plugins/k8s/dask).
To leverage this functionality, you need to enable the backend plugin in your deployment.
You can follow the steps mentioned in the {ref}`flyte:deployment-plugin-setup-k8s` section
to enable the Flyte Dask plugin for your deployment.

#### Step 2: Compute setup

Ensure that your Kubernetes cluster has sufficient resources available.
Depending on the resource requirements of your Dask job (including the job runner, scheduler and workers),
you may need to adjust the resource quotas for the namespace accordingly.

### Resource specification

It's recommended to define `limits` as this will establish the
`--nthreads` and `--memory-limit` parameters for the workers,
in line with the suggested practices by Dask
(refer to [best practices](https://kubernetes.dask.org/en/latest/kubecluster.html?highlight=--nthreads#best-practices)).
When configuring resources, the subsequent hierarchy is observed across all components of the Dask job,
which encompasses the job-runner pod, scheduler pod, and worker pods:

1. In the absence of specified resources, the
   [platform resources](https://github.com/flyteorg/flyte/blob/1e3d515550cb338c2edb3919d79c6fa1f0da5a19/charts/flyte-core/values.yaml#L520-L531)
   will be used.

2. When employing task resources, those will be enforced across all segments of the Dask job.
   You can achieve this using the following code snippet:

   > ```python
   > from flytekit import Resources, task
   > from flytekitplugins.dask import Dask
   >
   > @task(
   >   task_config=Dask(),
   >   limits=Resources(cpu="1", mem="10Gi")  # Applied to all components
   > )
   > def my_dask_task():
   >    ...
   > ```

3. When resources are designated for individual components, they hold the highest precedence.

   > ```python
   > from flytekit import Resources, task
   > from flytekitplugins.dask import Dask, Scheduler, WorkerGroup
   >
   > @task(
   >   task_config=Dask(
   >       scheduler=Scheduler(
   >           limits=Resources(cpu="1", mem="2Gi"),  # Applied to the job pod
   >       ),
   >       workers=WorkerGroup(
   >           limits=Resources(cpu="4", mem="10Gi"), # Applied to the scheduler and worker pods
   >       ),
   >   ),
   > )
   > def my_dask_task():
   >    ...
   > ```

### Images

By default, all components of the deployed `dask` job (job runner pod, scheduler pod and worker pods) will all use the
the image that was used while registering (this image should have `dask[distributed]` installed in its Python
environment). This helps keeping the Python environments of all cluster components in sync.
However, there is the possibility to specify different images for the components. This allows for use cases such as using
different images between tasks of the same workflow. While it is possible to use different images for the different
components of the `dask` job, it is not advised, as this can quickly lead to Python environments getting our of sync.

As the default behavior, all components of the deployed Dask job,
including the job runner pod, scheduler pod and worker pods,
will employ the image that was utilized during registration.
This image must have `dask[distributed]` installed in its Python environment,
ensuring consistency across the Python environments of all cluster components.

However, there exists the option to specify distinct images for these components.
This accommodation caters to scenarios where diverse images are required for tasks within the same workflow.
It is important to note that while it is technically possible to implement varying images
for different components of the dask job, this approach is not recommended.
Doing so can rapidly lead to discrepancies in Python environments.

> ```python
> from flytekit import Resources, task
> from flytekitplugins.dask import Dask, Scheduler, WorkerGroup
>
> @task(
>   task_config=Dask(
>       scheduler=Scheduler(
>           image="my_image:0.1.0",  # Will be used by the job pod
>       ),
>       workers=WorkerGroup(
>           image="my_image:0.1.0", # Will be used by the scheduler and worker pods
>       ),
>   ),
> )
> def my_dask_task():
>    ...
> ```

### Environment variables

Environment variables configured within the `@task` decorator will be propagated to all components of the Dask job,
encompassing the job runner pod, scheduler pod and worker pods.

> ```python
> from flytekit import Resources, task
> from flytekitplugins.dask import Dask
>
> @task(
>   task_config=Dask(),
>   env={"FOO": "BAR"}  # Will be applied to all components
> )
> def my_dask_task():
>    ...
> ```

### Labels and annotations

Labels and annotations specified within a {ref}`launch plan <launch_plan>` will be inherited by all components of the dask job,
which include the job runner pod, scheduler pod and worker pods.

> ```python
> from flytekit import Resources, task, workflow, Labels, Annotations
> from flytekitplugins.dask import Dask
>
> @task(task_config=Dask())
> def my_dask_task():
>    ...
>
> @workflow
> def my_dask_workflow():
>    my_dask_task()
>
> # Labels and annotations will be passed on to all dask cluster components
> my_launch_plan = my_dask_workflow.create_launch_plan(
>   labels=Labels({"myexecutionlabel": "bar", ...}),
>   annotations=Annotations({"region": "SEA", ...}),
> )
> ```

### Interruptible tasks

The Dask backend plugin offers support for execution on interruptible nodes.
When `interruptible==True`, the plugin will incorporate the specified tolerations and node selectors into all worker pods.
It's important to be aware that neither the job runner nor the scheduler will be deployed on interruptible nodes.

> ```python
> from flytekit import Resources, task, workflow, Labels, Annotations
> from flytekitplugins.dask import Dask
>
> @task(
>   task_config=Dask(),
>   interruptible=True,
> )
> def my_dask_task():
>    ...
> ```

## Run the example on the Flyte cluster

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote dask_example.py \
  hello_dask --size 1000
```

```{auto-examples-toc}
dask_example
```
