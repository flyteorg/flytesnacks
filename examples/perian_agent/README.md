# PERIAN Job Platform Agent

Flyte Agent plugin for executing Flyte tasks on PERIAN Job Platform (perian.io). PERIAN allows the serverless execution of any task on servers aggregated from multiple cloud providers.

Example usage:

```{auto-examples-toc}
@task(container_image=image_spec,
      task_config=PerianConfig(
          accelerators=1,
          accelerator_type="A100",
      ))
def perian_hello(name: str) -> str:
    return f"hello {name}!"
```

To get started with PERIAN, see the [PERIAN documentation](https://perian.io/docs/overview) and the [PERIAN Flyte Agent documentation](https://perian.io/docs/flyte-getting-started).

## Agent Setup

Consult the [PERIAN Flyte Agent setup guide](https://perian.io/docs/flyte-setup-guide).
