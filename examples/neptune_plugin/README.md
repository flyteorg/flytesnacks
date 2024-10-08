(neptune)=

# Neptune

```{eval-rst}
.. tags:: Integration, Data, Metrics, Intermediate
```

[Neptune](https://neptune.ai/) is an experiment tracker for large-scale model training. It allows AI researchers to monitor their model training in real time, visualize and compare experiments, and collaborate on them with a team. This plugin enables seamless use of Neptune within Flyte by configuring links between the two platforms. You can find more information about how to use Neptune in their [documentation](https://docs.neptune.ai/).

## Installation

To install the Flyte Neptune plugin, , run the following command:

```bash
pip install flytekitplugins-neptune
```

## Example usage

For a usage example, see the {doc}`Neptune example <neptune_example>`.

## Local testing

To run {doc}`Neptune example <neptune_example>` locally:

1. Create an account on [Neptune](https://neptune.ai/).
2. Create a project on Neptune.
3. In the example, set `NEPTUNE_PROJECT` to your project name.
4. Add a secret using [Flyte's Secrets manager](https://docs.flyte.org/en/latest/user_guide/productionizing/secrets.html) with `key="neptune-api-token"` and `group="neptune-api-group"`
5. If you want to see the dynamic log links in the UI, then add the configuration in the next section.

## Flyte deployment configuration

To enable dynamic log links, add the plugin to Flyte's configuration file:
```yaml
plugins:
  logs:
    dynamic-log-links:
      - neptune-run-id:
          displayName: Neptune
          templateUris: "{{ .taskConfig.host }}/{{ .taskConfig.project }}?query=(%60flyte%2Fexecution_id%60%3Astring%20%3D%20%22{{ .executionName }}-{{ .nodeId }}-{{ .taskRetryAttempt }}%22)&lbViewUnpacked=true"
```

```{auto-examples-toc}
neptune_example
```
