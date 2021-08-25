# Run the Workflow Locally

Let's use Flytekit Python SDK to run the workflow. This library helps in authoring, deploying, and testing the workflows.

First, install the flytekit library. To do so, run the command:
`pip install flytekit --upgrade`{{execute HOST1}}

The example that you would be working on must have been already cloned in the workspace, so just `cd` to the `ml_training/pima_diabetes` directory and install all the requirements.
`cd ml_training/pima_diabetes/`{{execute HOST1}}
`pip install -r requirements.txt`{{execute HOST1}}

`cd ../`{{execute HOST1}}

**Note**: You can find the Flyte entities -- `@task` and `@workflow` in the `ml_training/diabetes.py` file. `@task` is a Flyte task. It is the building block of Flyte that encapsulates the users' code. `@workflow` is a declarative entity that constructs a DAG of tasks using the data flow between tasks. To know more about Flyte's entities, refer to the [concepts guide](https://docs.flyte.org/en/latest/concepts/basics.html).

Now, the workflow can be run locally, simply by running it as a Python script.
`python3 pima_diabetes/diabetes.py`{{execute HOST1}}
