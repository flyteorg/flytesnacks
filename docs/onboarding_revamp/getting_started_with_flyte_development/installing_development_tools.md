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

(getting_started_installing_development_tools)=

# Installing development tools

To create and run workflows in Flyte, you must install Python, flytekit, flytectl, and Docker. Installing conda or another Python virtual environment manager is optional, but strongly recommended.

### Install Python

Python versions 3.8x - 3.10x are supported. [TK - note what version is used in Flyte docs and therefore recommended]

If you already have Python installed, you can use conda or pyenv to install the recommended version.

### Install Conda (or another Python virtual environment manager)

We strongly recommend installing [Conda](https://docs.conda.io/projects/conda/en/stable/) via miniconda to manage Python versions and virtual environments. Conda is used throughout the Flyte documentation.

You can also use another virtual environment manager, such as `[pyenv](https://github.com/pyenv/pyenv)` or `[venv](https://docs.python.org/3/library/venv.html)`.

### Install Flytekit

[TK - do we want people to set up a virtual environment before installing Flytekit? If so, the venv will be tied to a specific project]

### Install `flytectl`

You must install `flytectl` to start and configure a local Flyte cluster, as well as register workflows to a Flyte cluster.

[TK - Union docs have switcher for different OSes]

### Install Docker

[Install Docker](https://docs.docker.com/get-docker/) and ensure that you
have the Docker daemon running. [TK - link to docs to help folks get Docker daemon running, if need be]

Flyte supports any [OCI-compatible](https://opencontainers.org/) container
technology (like [Podman](https://podman.io/),
[LXD](https://linuxcontainers.org/lxd/introduction/), and
[Containerd](https://containerd.io/)), but
for the purpose of this documentation, `flytectl` uses Docker to spin up a local
Kubernetes cluster so that you can interact with it on your machine. [TK - be more specific here -- `flytectl demo start` uses Docker]
