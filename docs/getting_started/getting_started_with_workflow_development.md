---
# override the toc-determined page navigation order
prev-page: getting_started/quickstart_guide
prev-page-title: Quickstart guide
---

(getting_started_with_workflow_development)=

# Getting started with workflow development

Machine learning engineers, data engineers, and data analysts represent the processes that consume, transform, and output data with directed acyclic graphs (DAGs). In this section, you will learn how to create a Flyte project to contain the workflow code that implements your DAG, as well as the configuration files needed to package the code to run on a local or remote Flyte cluster.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Installing development tools <installing_development_tools>`
  - Install the tools needed to create Flyte projects and run workflows and tasks.
* - {doc}`Creating a Flyte project <creating_a_flyte_project>`
  - Create a Flyte project that contains workflow code and necessary configuration files.
* - {doc}`Running workflows locally <running_workflows_locally>`
  - Execute workflows locally both on a local cluster and not. TK - need better language here
```

```{toctree}
:maxdepth: -1
:hidden:

installing_development_tools
creating_a_flyte_project
flyte_project_components
running_workflows_locally
```
