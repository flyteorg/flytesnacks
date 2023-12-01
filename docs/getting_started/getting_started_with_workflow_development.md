---
# override the toc-determined page navigation order
prev-page: getting_started/quickstart_guide
prev-page-title: Quickstart guide
---

(getting_started_with_workflow_development)=

# Getting started with workflow development

At the heart of machine learning, data engineering, and data analytics is the directed acyclic graph (DAG) of processes that consume, transform, and output data. Flyte enables you to develop and test your DAGs locally in a production-like environment by creating a Flyte project to contain the task and workflow code that defines your DAG, as well as the configuration files needed to package your code to run on a local or remote Flyte cluster.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Installing development tools <getting_started_installing_development_tools>`
  - Install the tools needed to create Flyte projects and run workflows and tasks.
* - {doc}`Creating a Flyte project <getting_started_creating_a_flyte_project>`
  - Create a Flyte project that contains workflow code and configuration files needed to package the code to run on a local or remote Flyte cluster.
* - {doc}`Running workflows locally <getting_started_running_workflows_locally>`
  - Execute workflows locally both on a local cluster and not.
```

```{toctree}
:maxdepth: -1
:hidden:

installing_development_tools
creating_a_flyte_project
flyte_project_components
running_workflows_locally
```
