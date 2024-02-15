# Memory Machine Cloud

```{eval-rst}
.. tags:: AWS, GCP, AliCloud, Integration, Advanced
```

[MemVerge](https://memverge.com/) [Memory Machine Cloud](https://www.mmcloud.io/) (MMCloud)—available on AWS, GCP, and AliCloud—empowers users to continuously optimize cloud resources during runtime, safely execute stateful tasks on spot instances, and monitor resource usage in real time. These capabilities make it an excellent fit for long-running batch workloads. Flyte can be integrated with MMCloud, allowing you to execute Flyte tasks using MMCloud.

There are two implementations of the MMCloud integration:

* **{ref}`MMCloud agent <mmcloud_agent>`:** This implementation uses the agents framework (TK - link to agents guide). We strongly recommend using the MMCloud agent rather than the plugin, as agents can be tested locally without running the Flyte backend, are designed to be scalable, can handle large workloads efficiently, and decrease load on FlytePropeller.
* **{ref}`MMCloud plugin <databricks_plugin>`:** This implementation uses the legacy plugin framework. Only use this documentation if you have already configured your Flyte deployment to use the plugin. If you are using the plugin, we highly recommend migrating to the agent framework version instead, if possible.


```{toctree}
:maxdepth: -1
:hidden:

mmcloud_agent
mmcloud_plugin
example
```
