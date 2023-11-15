# %% [markdown]
# # File Sensor
#
# This example shows how to use the `FileSensor` to detect files appearing in your local or remote filesystem.
#
# First, import the required libraries.

# %%
from flytekit import task, workflow
from flytekit.sensor.file_sensor import FileSensor

# %% [markdown]
# Next, create a FileSensor task.

# %%
sensor = FileSensor(name="test_file_sensor")

# %% [markdown]
# To use the FileSensor created in the previous step, you must specify the path parameter. In the sandbox, you can use the S3 path.


# %%
@task()
def t1():
    print("SUCCEEDED")


@workflow()
def wf():
    sensor(path="s3://my-s3-bucket/file.txt") >> t1()


if __name__ == "__main__":
    wf()

# %% [markdown]
# You can also use the S3 or GCS file system.
# We have already set the minio credentials in the agent by default. If you test the sandbox example locally, you will need to set the AWS credentials in your environment variables.
#
# ```{prompt} bash
# export FLYTE_AWS_ENDPOINT="http://localhost:30002"
# export FLYTE_AWS_ACCESS_KEY_ID="minio"
# export FLYTE_AWS_SECRET_ACCESS_KEY="miniostorage"
# ```
