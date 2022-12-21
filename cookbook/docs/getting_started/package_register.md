---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(getting_started_package_register)=

# Packaging and Registering Workflows

```{admonition} Prerequisites
:class: important

Follow the [installation](getting_started_installation) instructions.
```

In the {ref}`Initializing a Flyte project <getting_started_init_flyte_project>`
guide we created a minimal Flyte project.

In this guide, you'll learn how to package and register your tasks and
workflows to a Flyte cluster. This will enable you to scale your workloads with
larger memory and compute requirements, schedule your workflows to run on a
pre-defined cadence, and leverage other compute platforms like Spark, Ray, and
Sagemaker.

## Flyte Demo Cluster

In the {ref}`Introduction to Flyte <getting_started_flyte_cluster>` guide you
spun up a local Flyte cluster with:

```{prompt} bash $
flytectl demo start
```

You can access the 

## Containerizing your project


## Flyte configuration


## Common registration patterns


## Custom Python dependencies


## Using multiple images in your workflow


## CI/CD with Flyte and Github Actions
