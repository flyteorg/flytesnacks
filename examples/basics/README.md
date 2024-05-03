# Basics

These examples demonstrate the basic building blocks of Flyte using [`flytekit`](https://docs.flyte.org/en/latest/api/flytekit/docs_index.html). `flytekit` is a Python SDK for developing Flyte workflows and
tasks, and can be used generally, whenever stateful computation is desirable. `flytekit` workflows and tasks are completely runnable locally, unless they need some advanced backend functionality like starting a distributed Spark cluster.

These examples cover writing Flyte tasks, assembling them into workflows,
running bash scripts, and documenting workflows.
