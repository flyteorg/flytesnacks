(sensor)=

# Sensor

```{eval-rst}
.. tags:: Data, Basic
```

## Run the example on the Flyte cluster

To run the provided example on the Flyte cluster, use the following command:

```
pyflyte run --remote \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/sensor/sensor/file_sensor_example.py wf
```

## Usage

For an example of how to use the `FileSensor` to detect the appearance of files in a local or remote filesystem, see the {doc}`"File sensor example" <file_sensor_example>` example page.

```{toctree}
:hidden:

file_sensor_example
```
