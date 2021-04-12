What are Backend Plugins?
=========================
Flyte backend plugins are more involved and implementation needs writing code in ``Golang`` that gets plugged into the Flyte backend engine. These plugins are statically loaded into the FlytePropeller. The contract for the plugin can be encoded in any serialization format - e.g. JSON, OpenAPI, protobuf. The community in general prefers using protobuf.
Once the backend plugin is implemented, any language SDK can be implemented to provide a specialized interface for the user.

Examples

#. `Sagemaker <https://github.com/lyft/flytekit/tree/master/plugins/awssagemaker>`_
#. `K8s Spark <https://github.com/lyft/flytekit/tree/master/plugins/spark>`_

Native Backend Plugins
^^^^^^^^^^^^^^^^^^^^^^^
Native Backend Plugins are plugins that can be executed without any external service
dependencies. The compute is orchestrated by Flyte itself, within its
provisioned kubernetes clusters. Some examples of native plugins are

#. Python functions
#. K8s Containerized Spark
#. Array Tasks
#. Pod Tasks
#. K8s native distributed Pytorch training using Kubeflow Pytorch Operator
#. K8s native distributed Tensorflow training using Kubeflow TF Operator

External Service Backend Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. AWS Sagemaker Training
#. AWS Batch
#. Qubole Hive