(plugins-spark-k8s)=

# Spark

```{eval-rst}
.. tags:: Spark, Integration, DistributedComputing, Data, Advanced
```

Flyte has the capability to directly execute Spark jobs on a Kubernetes Cluster.
The cluster handles the lifecycle, initiation and termination of virtual clusters.
It harnesses the open-source [Spark on Kubernetes operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator)
and can be enabled without requiring any service subscription.
This functionality is akin to operating a transient spark cluster
— a cluster type established specifically for a Spark job and taken down upon completion.

While these clusters are optimal for production workloads, they do come with the additional cost of setup and teardown.
In the Flyte environment, this cost is spread out over time due to the swiftness of creating pods compared to a full machine.
However, keep in mind that the performance might be impacted by the need to download Docker images, and starting a pod is not as immediate as running a process.

With Flytekit, you can compose PySpark code natively as a task.
The Spark cluster will be automatically configured using the specified Spark configuration.
The examples provided in this section offer a hands-on tutorial for writing PySpark tasks.

:::{note}
This plugin has been rigorously tested at scale, successfully managing more than 100,000 Spark Jobs through Flyte at Lyft.
However, please bear in mind that this functionality requires a significant Kubernetes capacity and meticulous configuration.

For optimal results, we highly recommend adopting the
[multi-cluster mode](https://docs.flyte.org/en/latest/deployment/configuration/performance.html#multi-cluster-mode).
Additionally, consider enabling {std:ref}`resource quotas <deployment/configuration/general:configurable resource types>`
for Spark Jobs that are both large in scale and executed frequently.

Nonetheless, it is important to note that extremely short-duration jobs might not be the best fit for this setup.
In such cases, utilizing a pre-spawned cluster could be more advantageous.
A job can be considered "short" if its runtime is less than 2 to 3 minutes.
In these situations, the cost of initializing pods might outweigh the actual execution cost.
:::

## Why use Kubernetes Spark?

Managing Python dependencies can be challenging, but Flyte simplifies the process
by enabling easy versioning and management of dependencies through containers.
The Kubernetes Spark plugin extends the benefits of containerization to Spark without
requiring the management of specialized Spark clusters.

Pros:

1. Simple to get started, providing complete isolation between workloads.
2. Each job runs in isolation with its own virtual cluster, eliminating the complexities of dependency management.
3. Flyte takes care of all the management tasks.

Cons:

1. Short-running, bursty jobs may not be the best fit due to container overhead.
2. Interactive Spark capabilities are not available with Flyte Kubernetes Dask;
   instead, it is better suited for running adhoc and scheduled jobs.

## Implementation details

### Step 1: Deploy Spark plugin in the Flyte backend

Flyte Spark employs the Spark on K8s operator in conjunction with a bespoke
[Flyte Spark Plugin](https://pkg.go.dev/github.com/flyteorg/flyteplugins@v0.5.25/go/tasks/plugins/k8s/spark).

This plugin serves as a backend component and necessitates activation within your deployment.
To enable it, follow the instructions outlined in the {ref}`flyte:deployment-plugin-setup-k8s` section.

:::{note}
Refer to [this guide](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/gcp.md) to use GCP instead of AWS.
:::

### Step 2: Environment Setup

Install `flytekitplugins-spark` using `pip` in your environment.

```bash
pip install flytekitplugins-spark
```

:::{note}
To enable Flyte to build the Docker image for you using `ImageSpec`, install `flytekitplugins-envd`.
:::

Ensure that your Kubernetes cluster has sufficient resources available.
Depending on the resource requirements of your Spark job across the driver and executors,
you may need to adjust the resource quotas for the namespace accordingly.

### Step 3: Optionally, set up visibility

Whenever a Spark job is executed, you have the opportunity to access a Spark application UI link for
real-time job monitoring. Additionally, for past executions, you can leverage the
Spark history server to access the stored history of Spark executions.

Furthermore, Flyte offers the capability to generate direct links to both the Spark driver logs and individual Spark executor logs.

These Spark-related features, including the Spark history server and Spark UI links, are seamlessly displayed on the Flyte Console.
Their availability is contingent upon the following configuration settings:

#### Configure the Spark history link within the UI

To access the Spark history UI link within the Flyte Console,
it's necessary to configure a variable in the Spark section of the Flyteplugins configuration.
Here's an example of how to set it up:

```
plugins:
  spark:
    spark-history-server-url: <root-url-forspark-history server>
```

You can explore various configuration options by referring to
[this link](https://github.com/flyteorg/flyteplugins/blob/master/go/tasks/plugins/k8s/spark/config.go).

#### Configure the Spark application UI

To obtain a link for the ongoing Spark drivers and the Spark application UI,
you must set up Kubernetes to allow wildcard ingress access using `*.my-domain.net`.
Additionally, you should configure the Spark on Kubernetes operator to
establish a new ingress route for each application.

This can be achieved through the `ingress-url-format` command-line option of the Spark Operator.
You can find more details about this option in the source code
[here](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/d38c904a4dd84e849408153cdf4d7a30a7be5a07/main.go#L62).

#### Configure the Spark driver and executor logs

The logs can be configured by adjusting the `logs` configuration within the Spark plugin settings.
The Spark plugin utilizes the same default log configuration outlined in the section on {ref}`configure-logging`.

The SparkPlugin offers the capability to segregate user (Spark user code) and system (Spark core logs) logs,
thus enhancing visibility into Spark operations.
This is, however, feasible only if you can route the spark user logs separately from the core logs.
It's important to note that Flyte does not perform automatic log separation. You can review the configuration structure
[here](https://github.com/flyteorg/flyteplugins/blob/master/go/tasks/plugins/k8s/spark/config.go#L31-L36).

- _Mixed_: Provides unseparated logs from the Spark driver (combining both user and system logs), following the standard structure of all log plugins.
  You can obtain links to the Kubernetes dashboard or a preferred log aggregator as long as it can generate standardized links.
- _User_: Offers logs from the driver with separation (subject to log separation availability).
- _System_: Covers logs from executors, typically without individual links for each executor;
  instead, it provides a prefix where all executor logs are accessible.
- _AllUser_: Encompasses all user logs across spark-submit, driver and executor.

Log configuration example:

```yaml
plugins:
  spark:
    logs:
      user:
        kubernetes-enabled: true
        kubernetes-url: <the existing k8s url you have in the main logs section>
      mixed:
        cloudwatch-enabled: true
        cloudwatch-template-uri: "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=<LogGroupName>;prefix=var.log.containers.{{.podName}};streamFilter=typeLogStreamPrefix"
      system:
        cloudwatch-enabled: true
        cloudwatch-template-uri: "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=<LogGroupName>;prefix=system_log.var.log.containers.{{.podName}};streamFilter=typeLogStreamPrefix"
      all-user:
        cloudwatch-enabled: true
        cloudwatch-template-uri: "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=<LogGroupName>;prefix=var.log.containers.{{.podName}};streamFilter=typeLogStreamPrefix"
```

#### Additional configuration

The Spark plugin provides support for a range of extended configuration options.
For instance, if you wish to enable specific Spark features as defaults for all Spark applications,
you can apply default Spark configurations.

For more comprehensive information, please consult the [configuration structure](https://github.com/flyteorg/flyteplugins/blob/c528bb88937b4732c9cb5537ed8ea6943ff4fb56/go/tasks/plugins/k8s/spark/config.go#L24-L29).

## Run the examples on the Flyte cluster

To run the provided examples on the Flyte cluster, use any of the following commands:

```
pyflyte run --remote pyspark_pi.py my_spark
```

```
pyflyte run --remote dataframe_passing.py \
  my_smart_structured_dataset
```

(spark-examples)=

```{auto-examples-toc}
pyspark_pi
dataframe_passing
```
