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

# override the toc-determined page navigation order
next-page: getting_started/quickstart-guide
next-page-title: Quickstart guide
---

(getting_started_index)=

# About Flyte

Flyte is a workflow orchestrator that seamlessly unifies data engineering, machine learning, and data analytics stacks for building robust and reliable applications. Flyte features:
* Reproducible, repeatable workflows
* Strongly typed interfaces
* Structured datasets to enable easy conversion of dataframes between types, and column-level type checking
* Easy movement of data between local and cloud storage
* Easy tracking of data lineages
* Built-in data and artifact visualization

For a full list of feature, see the [Flyte features page](https://flyte.org/features).

[TK - decide where to put link to hosted sandbox https://sandbox.union.ai/]

## Basic Flyte components

Flyte is made up of a User Plane, Control Plane, and Data Plane.
* The **User Plane** consists of FlyteKit, the FlyteConsole, and Flytectl, which assist in interacting with the core Flyte API. Tasks, workflows, and launch plans are part of the User Plane.
* The **Control Plane** implements the core Flyte API and serves all client requests coming from the User Plane. The Control Plane stores information such as current and past running workflows, and provides that information upon request. It also accepts requests to execute workflows, but offloads the work to the Data Plane.
* The **Data Plane** accepts workflow requests from the Control Plane and guides the workflow to completion, launching tasks on a cluster of machines as necessary based on the workflow graph. The Data Plane sends status events back to the Control Plane so that information can be stored and surfaced to end users.

## Next steps

* To quickly create and run a Flyte workflow, follow the [Quickstart guide](TK-link), then read "[Getting started with Flyte development](TK-link)".
* To create a Flyte Project with lightweight directory structure and configuration files, go to "[Getting started with Flyte development](TK-link)".