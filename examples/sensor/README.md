(sensor)=

# Sensor

```{eval-rst}
.. tags:: Data, Basic
```

## Usage

For an example of detecting a file with the `FileSensor`, see the {doc}`file sensor example <file_sensor_example>`.

### Run the file senseor example on a Flyte cluster

To run the provided example on a Flyte cluster, use the following command:

```
pyflyte run --remote \
  https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/sensor/sensor/file_sensor_example.py wf
```

## Deployment configuration

```{note}
If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.
```

To enable the sensor agent in your Flyte deployment, see the {ref}`sensor agent deployment documentation<deployment-agent-setup-sensor>`.

```{toctree}
:maxdepth: -1
:hidden:
file_sensor_example
```
