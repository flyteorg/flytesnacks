# %% [markdown]
# # File Sensor
#
# This example shows how to use the `FileSensor` to detect files appearing in your local or remote filesystem.
#
# To begin, import the required libraries.

# %%
from flytekit import task, workflow
from flytekit.sensor.file_sensor import FileSensor

# %% [markdown]
# Create a FileSensor task.
#
# The sensor will find the file at the given path.
#
# You can also use the S3 file system or GCS file system.

# %%
sensor = FileSensor(name="test_file_sensor")

# %% [markdown]
# You have to specify the `path` parameter.
#
# In the sandbox, you can use the s3 path.
#
# We have already set the minio credentials in the agent by default.
#
# If you test it locally, you have to set the credentials to your environment variables.
# ```{prompt} bash
# export FLYTE_AWS_ENDPOINT="http://localhost:30002"
# export FLYTE_AWS_ACCESS_KEY_ID="minio"
# export FLYTE_AWS_SECRET_ACCESS_KEY="miniostorage"
# ```


# %%
@task()
def t1():
    print("SUCCEEDED")


@workflow()
def wf():
    sensor(path="s3://my-s3-bucket/file.txt") >> t1()


if __name__ == "__main__":
    wf()
