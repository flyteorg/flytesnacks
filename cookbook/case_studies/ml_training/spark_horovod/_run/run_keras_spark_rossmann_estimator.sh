# shellcheck shell=ksh
pyflyte run --remote --image ghcr.io/flyteorg/flytecookbook:spark_horovod-latest keras_spark_rossmann_estimator.py horovod_spark_wf
