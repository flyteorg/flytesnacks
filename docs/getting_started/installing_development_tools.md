---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

(getting_started_installing_development_tools)=

# Installing development tools

To create and run workflows in Flyte, you must install Python, flytekit, flytectl, and Docker. Installing conda or another Python virtual environment manager is optional, but strongly recommended.

## Install Python

Python versions 3.8x - 3.10x are supported. [TK - is this accurate?]

If you already have Python installed, you can use conda or pyenv to install the recommended version.

## Install Conda (or another Python virtual environment manager)

We strongly recommend installing [conda](https://docs.conda.io/projects/conda/en/stable/) via [miniconda](https://docs.conda.io/projects/miniconda/en/latest/) to manage Python versions and virtual environments. Conda is used throughout the Flyte documentation.

You can also use another virtual environment manager, such as [pyenv](https://github.com/pyenv/pyenv) or [venv](https://docs.python.org/3/library/venv.html).

## Install Flytekit

To install or upgrade flytekit, on the command line, run the following:

```{prompt} bash
pip install -U flytekit
```

[TK - do we want people to create a virtual environment before installing Flytekit? If so, should that venv be tied to a particular Flyte project?]

## Install `flytectl`

You must install `flytectl` to start and configure a local Flyte cluster, as well as register workflows to a local or remote Flyte cluster.

````{tabbed} macOS
To use Homebrew, on the command line, run the following:

```{prompt} bash $
brew install flyteorg/homebrew-tap/flytectl
```

To use `curl`, on the command line, run the following:

```{prompt} bash $
curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin
```

To download manually, see the [flytectl releases](https://github.com/flyteorg/flytectl/releases).
````

````{tabbed} Linux
To use `curl`, on the command line, run the following:

```{prompt} bash $
curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin
```

To download manually, see the [flytectl releases](https://github.com/flyteorg/flytectl/releases).
````

````{tabbed} Windows
To use `curl`, in a Linux shell (such as [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)), on the command line, run the following:

```{prompt} bash $
curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin
```

To download manually, see the [flytectl releases](https://github.com/flyteorg/flytectl/releases).
````


## Install Docker

[Install Docker](https://docs.docker.com/get-docker/) and ensure that you
have the Docker daemon running. [TK - link to docs to help folks get Docker daemon running, if need be]

Flyte supports any [OCI-compatible](https://opencontainers.org/) container technology (like [Podman](https://podman.io/), [LXD](https://linuxcontainers.org/lxd/introduction/), and [Containerd](https://containerd.io/)), but for the purpose of this documentation, `flytectl` uses Docker to spin up a local Kubernetes cluster so that you can interact with it on your machine. [TK - be more specific here -- `flytectl demo start` uses Docker]
