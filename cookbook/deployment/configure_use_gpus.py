"""
.. _configure-gpus:

Configuring Flyte to access GPUs
----------------------------------

Along-with the simpler resources like CPU/Memory, you may want to configure and access GPU resources as well. Flyte,
allows you to configure the GPU access poilcy for your cluster. GPU's are expensive and it would not be ideal to
treat machines with GPU's equally to machines with CPU's only. You may want to reserve machines with GPU's to tasks
that explicitly request for GPU's. To achieve this Flyte use the kubernetes concept of `taints and tolerations <https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/>`_.

You can configure flyte backend, to automatically schedule your task onto a node with GPU's by tolerating specific taints.
This configuration is controlled under generic k8s plugin configuration, found `here <https://github.com/flyteorg/flyteplugins/blob/master/go/tasks/pluginmachinery/flytek8s/config/config.go#L105-L107>`_

The idea of this configuration is that whenever a task that can execute on Kubernetes, requests for GPU's it automatically
adds the matching toleration for that resource (in this case ``gpu``) to the generated PodSpec.
As it follows here, you can configure it to access specific resources using the tolerations, for all resources supported by
Kubernetes.

An example configuration looks like,

.. code-block:: yaml

    plugins:
        k8s:
            resource-tolerations:
                gpu:

"""