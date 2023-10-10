# %% [markdown]
# # Sensoring file
#
# This example shows how to use the `SensorTask` to execute a query in Sensor.
#
# To begin, import the required libraries.
# %%
from flytekit import task, workflow
from flytekit.sensor.file_sensor import FileSensor

# %% [markdown]
# Create a Sensor task.
# The sensor will find the file at the given path.
# You can also use s3 file system.
# %%
sensor = FileSensor(name="test_sensor")

# %% [markdown]
# :::{note}
# You have to specify the `path` parameter.
# %%
@task()
def t1():
    print("SUCCEEDED")


@workflow()
def wf():
    sensor(path="/tmp/123") >> t1()


if __name__ == "__main__":
    wf()
