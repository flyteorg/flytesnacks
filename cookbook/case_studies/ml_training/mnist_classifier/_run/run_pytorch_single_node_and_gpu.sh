# shellcheck shell=ksh
pyflyte run --remote --image ghcr.io/flyteorg/flytecookbook:mnist_classifier-latest pytorch_single_node_and_gpu.py pytorch_training_wf
