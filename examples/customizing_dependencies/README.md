# Customizing Dependencies

As a container-native orchestration tool, all Flyte tasks are executed within isolated containers. The `flytekit` Python SDK enables you to configure these tasks for your needs
easily, be it running a raw container with arbitrary commands, specifying multiple
container images in a single workflow, injecting secrets into a container, or using
spot instances.

```{auto-examples-toc}
image_spec
raw_container
multi_images
```
