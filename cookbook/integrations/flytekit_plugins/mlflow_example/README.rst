.. mlflow:

MLflow
======

.. tags:: Integration, Data, Metrics, Intermediate

First, install the Flyte MLflow plugin:

.. prompt:: bash $
    pip install flytekitplugins-mlflow


The MLflow Tracking component is an API and UI for logging parameters,
code versions, metrics, and output files when running your machine learning code and for later visualizing the results

To log the metrics and parameters to Flyte deck, add :py:func:`@mlflow_autolog <flytekitplugins.mlflow.mlflow_autolog>` to the task. For example

.. code:: python

    @task(disable_deck=False)
    @mlflow_autolog(framework=mlflow.keras)
    def train_model(epochs: int):
    ...

To log the metric and parameters to a remote mlflow server, add default environment variable `MLFLOW_TRACKING_URI <https://mlflow.org/docs/latest/tracking.html#logging-to-a-tracking-server>`__ to the flytepropeller config map.

.. prompt:: bash $
    kubectl edit cm flyte-propeller-config

.. code:: yaml

    plugins:
      k8s:
        default-cpus: 100m
        default-env-vars:
        - MLFLOW_TRACKING_URI: postgresql+psycopg2://postgres:@postgres.flyte.svc.cluster.local:5432/flyteadmin

.. figure:: https://user-images.githubusercontent.com/37936015/209251641-02f77a71-b3f5-4efb-a87b-43f283b2de0b.png
  :alt: MLflow UI
  :class: with-shadow