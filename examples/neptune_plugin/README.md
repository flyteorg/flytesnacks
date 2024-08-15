(neptune)=

# Neptune

```{eval-rst}
.. tags:: Integration, Data, Metrics, Intermediate
```

Neptune is the MLOps stack component for experiment tracking. It offers a single place to log, compare, store, and collaborate on experiments and models. This plugin enables seamless use of Neptune within Flyte by configuring links between the two platforms.

First, install the Flyte Neptune plugin:

```bash
pip install flytekitplugins-neptune
```

To enable dynamic log links, add plugin to Flyte's configuration file:
```yaml
plugins:
  logs:
    dynamic-log-links:
      - neptune-run-id:
          displayName: Neptune
          templateUris: "{{ .taskConfig.host }}/{{ .taskConfig.project }}?query=(%60Flyte%20Execution%20ID%60%3Astring%20%3D%20%22{{ .executionName }}-{{ .nodeId }}-{{ .taskRetryAttempt }}%22)&lbViewUnpacked=true"
```

```{auto-examples-toc}
neptune_example
```
