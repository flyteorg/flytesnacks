MLflow
======

.. tags:: Integration, Data, Metrics, Intermediate

The MLflow Tracking component is an API and UI for logging parameters,
code versions, metrics, and output files when running your machine learning code and for later visualizing the results

MLflow is used by Flyte to automatically log the task's metrics and parameters to either Flyte Deck or MLflow server.

`<https://user-images.githubusercontent.com/37936015/200655711-8eb54757-cc08-4591-8f44-787cc4b0af66.png>`__
`<https://user-images.githubusercontent.com/37936015/200655752-fddfd0cd-26f2-4ccf-914a-08044c7c4dae.png>`__

To log the metrics and parameters to Flyte deck, add `@mlflow_autolog` to the task. For example
```python
@task(disable_deck=False)
@mlflow_autolog(framework=mlflow.keras)
def train_model(epochs: int):
    ...
```

To log the metric and parameters to a remote mlflow server, add default env (`MLFLOW_TRACKING_URI <https://mlflow.org/docs/latest/tracking.html#logging-to-a-tracking-server>`__) to the flytepropeller config map.
```bash
    plugins:
      k8s:
        default-cpus: 100m
        default-env-vars:
        - MLFLOW_TRACKING_URI: postgresql+psycopg2://postgres:@postgres.flyte.svc.cluster.local:5432/flyteadmin
```

`<https://user-images.githubusercontent.com/37936015/209251641-02f77a71-b3f5-4efb-a87b-43f283b2de0b.png>`__
