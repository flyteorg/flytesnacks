# Flytekit Cookbook

This is a collection of short "how to" articles demonstrating the various capabilities and idiomatic usage of Flytekit.
Note this currently does not include articles/tid-bits on how to use the Flyte platform at large, though in the future we may expand it to that.


## Contents   
1. [Write and Execute a Task](recipes/task/README.md)
2. [Working with Types](recipes/types/README.md)
3. [Create a workflow from Tasks](recipes/workflows/README.md)
4. [Launch Plans](recipes/launchplans/README.md)
5. [Multiple Schedules for a Workflow](recipes/multi_schedules/README.md)
6. [Interact with Past Workflow / Task Executions](recipes/interaction/README.md)
7. [Dynamic Tasks](recipes/dynamictasks/README.md)
8. [Compose a Workflow from other workflows](recipes/compose/README.md)
9. [Dynamically Generate a Workflow at Runtime](recipes/dynamic_wfs/README.md)
10. [Tasks without flytekit or Using arbitrary containers](recipes/rawcontainers/README.md)
11. [Using Papermill & Jupyter notebook to author tasks](recipes/papermill/README.md)
12. [Executing pre-created tasks & workflows](recipes/fetch/README.md)
13. [Composing a Workflow from shared tasks and workflows](recipes/shared/README.md)
14. [Different container per task](recipes/differentcontainers/README.md)

## Setup

Follow instructions in the main Flyte documentation.

All the commands in this book assume that you are using Docker Desktop. If you are using minikube or another K8s deployment, the commands will need to be modified.

## Using Locally

Please ensure that you have a virtual environment installed and activated.

### Make Targets

* To build the image

```
make docker_build
```

* To register

```
make register_sandbox
```

The above commands will produce and use images with no registry in the name - it will just be `flytecookbook:<sha>`. If you would like to push to a registry like ECR or DockerHub, please prepend a `REGISTRY` to the commands. 

* To push the image

```
REGISTRY=docker.io/corp make docker_push
```
