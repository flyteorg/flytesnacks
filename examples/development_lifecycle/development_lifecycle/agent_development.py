# %% [markdown]
# # How To Develop Agent Plugin Service?
#
# ```{eval-rst}
# .. tags:: Extensibility, Contribute, Intermediate
# ```
#
# ## Why Plugin Service but not write the service within a task?
# Flyte can execute external web APIs in two ways: by writing the service within a task or by utilizing FlytePlugins.

# ### Writing the service within a task
# Suppose you have a workflow that requires the integration of a web API, like ChatGPT.
#
# You might have a Python code similar to the one below:
#
# ```python
# @task()
# def t1(input: str) -> str:
#     completion = openai.ChatCompletion.create(
#           model="gpt-3.5-turbo",
#           messages=[
#             {"role": "user", "content": input}
#           ]
#         )
#     return completion.choices[0].message
#
# @workflow
# def wf() -> str:
#     return t1(input="Your Input Message!")
# ```
#
# Here is how the task's lifecycle unfolds:
# 1. FlytePropeller initiates a pod to execute the task.
#
# 2. The task, running within the pod, calls the ChatGPT API.
#
# 3. After the task is completed, FlytePropeller terminates the pod.
#
# This process can be resource-intensive and also time-consuming, as initiating and terminating pods for each task execution consumes additional resources and needs much time.
#
# ### Utilizing FlytePlugins
# Let's analyze the example above and compare it to the code provided [here](https://docs.flyte.org/projects/cookbook/en/latest/auto_examples/bigquery_plugin/bigquery.html).
#
# ```python
# bigquery_task_no_io = BigQueryTask(
#     name="sql.bigquery.no_io",
#     inputs={},
#     query_template="SELECT 1",
#     task_config=BigQueryConfig(ProjectID="flyte"),
# )
#
#
# @workflow
# def no_io_wf():
#     return bigquery_task_no_io()
# ```
#
#
# In this example, the lifecycle of the bigquery task progresses as follows:
#
# 1. FlytePlugins invokes the BigQuery API, as seen [here](https://github.com/flyteorg/flyte/tree/master/flyteplugins/go/tasks/plugins/webapi/bigquery).
#
# This approach is notably quicker and more resource-efficient.
