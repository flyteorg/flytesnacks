[Back to Snacks Menu](../README.md)

# :books: Flytekit Cookbook (2nd Edition)

This is a collection of short "how to" articles demonstrating the various capabilities and idiomatic usage of Flytekit.
Note this currently does not include articles/tid-bits on how to use the Flyte platform at large, though in the future we may expand it to that.

Also note that this is different than the first cookbook we had written (also in this repo). It may be premature to consider this directory a second edition, but the style is a bit different.
This book is divided into four sections currently. The first three advance through increasingly complicated Flytekit examples, and the fourth deals with writing Flytekit as it relates to a Flyte deployment.
Also, this iteration of the cookbook is written in the literate programming style. That is, the contents of this directory should serve as both documentation, as well as a fully-functional Flyte workflow repo.

## :airplane: :closed_book: Built Book

The built documentation is available at https://flytecookbook.readthedocs.io/en/latest/.

## Using the Cookbook

The examples written in this cookbook are meant to used in few ways, as a reference to read if you have a specific question about a specific topic, as template to iterate on locally as many parts of Flytekit are built to be locally usable, and finally as test on your local (or EKS/GCP/etc K8s cluster). To make some simple changes to the code in this cookbook to just try things out, or to just see it run on your local cluster, the iteration cycle should be

1. Make your changes and commit (the steps below require a clean git tree).
1. Activate your Python virtual environment with the requirements installed.
1. `make docker_build` This will build the image tagged with just `flytecookbook:<sha>`, no registry will be prefixed.
1. `make register_sandbox` This will register the Flyte entities in this cookbook against your local installation.

If you are registering outside the sandbox, register entities using:
`flyte-cli register-files -p <myproject> -d development -v <gitsha> -h localhost:30081 [<my_files>]`

If you are just iterating locally, there is no need to push your Docker image. For Docker for Desktop at least, locally built images will be available for use in its K8s cluster.

If you would like to later push your image to a registry (Dockerhub, ECR, etc.), you can

```bash
REGISTRY=docker.io/corp make docker_push
```

### Setup

1. Follow instructions in the main Flyte documentation to set up a local Flyte cluster. All the commands in this book assume that you are using Docker Desktop. If you are using minikube or another K8s deployment, the commands will need to be modified.
1. Please also ensure that you have a Python virtual environment installed and activated, and have pip installed the requirements.
1. Use flyte-cli to create a project named `flytesnacks` (the name the Makefile is set up to use).
