############################################
Flyte Plugins
############################################

Flyte is designed to be highly extensible. Flyte can be extended in multiple ways

#. Flytekit only plugins: Plugins that are like executing a python function in a container
#. Flyte backend global plugins: Plugins that are independent of the SDK and enable backend capabilities in Flyte and are global for the entire deployment
#. Flyte custom container executions: Execute arbitrary containers - data is loaded into the container as files and read out of the containers. One can write c++ code, bash scripts and any containerized program
#. Bring your own SDK: the community would love to help you with your own ideas of building a new SDK. Ideas include - ``golang``, ``javascript/nodejs`` etc

Available SDKs:

#. `Flytekit <https://github.com/lyft/flytekit>`_ is the Python SDK for writing Flyte tasks and workflows and is optimized for Machine Learning pipelines and ETL workloads
#. `Flytekit-Java <https://github.com/spotify/flytekit-java>`_ is the Java/SCALA SDK optimized for ETL and data processing workloads

What are Flytekit [python] only plugins?
===========================================
Flytekit plugins are simple plugins that can be implemented purely in python, unit tested locally and allow extending Flytekit functionality. These plugins can be anything and for comparison can be thought of like Airflow Operators.
Data is automatically marshalled and unmarshalled into and out of the plugin and mostly users should implement :py:class:`flytekit.core.base_task.PythonTask` API, defined in flytekit.
This tutorial will illustrate how a plugin can be implemented with the help of an example.

Flytekit Plugins are lazily loaded and can be released independently like libraries. We follow a convention to name the plugin like
``flytekitplugins-*``, where * implies the capability. For example ``flytekitplugins-papermill`` enables users to author flytekit tasks using `Papermill <https://papermill.readthedocs.io/en/latest/>`_

Examples of flytekit only plugins:

#. Papermill implementation `flytekitplugins-papermill <https://github.com/lyft/flytekit/tree/master/plugins/papermill>`_
#. SQLite3 implementation `SQLite3 Queries <https://github.com/lyft/flytekit/blob/master/flytekit/extras/sqlite3/task.py>`_