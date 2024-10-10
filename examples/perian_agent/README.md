# PERIAN Job Platform Agent

The PERIAN Flyte Agent enables you to execute Flyte tasks on the [PERIAN Sky Platform](https://perian.io/). PERIAN allows the execution of any task on servers aggregated from multiple cloud providers.

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

## Agent setup

Consult the [PERIAN Flyte Agent setup guide](https://perian.io/docs/flyte-setup-guide).
