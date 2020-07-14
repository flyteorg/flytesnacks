# Simple PySpark Job as a Flyte Workflow

[Example: pyspark_pi.py](pyspark_pi.py)

## Introduction:

In this example, we run a simple PySpark job as part of a Flyte workflow. The Spark Job calculates the value of Pi and sets it as the output of the task.
This output is then consumed by a dependent python task which forms the other task in the workflow.

For PySpark Tasks, Flyte provides an an additional `spark_context` input in addition to the `workflow_parameters`. 
`spark_context` is deprecated and in future releases of flytekit, there is a plan to update Spark task to provide `spark_session` which is the unified entry-point for the Spark APIs.

If needed, users can convert `spark_context` to a `spark_session` like:

<code> 
sql_context = SQLContext(spark_context)

spark_session = sql_context.sparkSession
</code>
 



