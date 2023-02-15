---
# override the toc-determined page navigation order
prev-page: index
prev-page-title: Getting Started
---

(getting_started_fundamentals)=

# Flyte Fundamentals

This section of the **Getting Started** documentation will take you through the
fundamental concepts of Flyte: tasks, workflows, and launch plans.

You'll learn about the full development lifecycle of creating a project,
registering workflows, and running them on a demo Flyte cluster. These
guides will also walk you through how to visualize artifacts associated with
tasks, optimize them for scale and performance, and extend Flyte for your own
use cases.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`🔀 Tasks, Workflows and LaunchPlans <tasks_and_workflows>`
  - Create tasks as building blocks, compose them into workflows, and schedule
    them with launchplans.
* - {doc}`✨ Creating a Flyte Project <creating_flyte_project>`
  - Build a Flyte project from scratch and learn about the recommended project
    structure.
* - {doc}`🗄 Registering Workflows <package_register>`
  - Develop and deploy workflows to a local Flyte demo cluster.
* - {doc}`⏱ Running and Scheduling Workflows <run_schedule>`
  - Execute workflows programmatically and schedule them as cron jobs.
* - {doc}`📊 Visualizing Artifacts <visualizing_artifacts>`
  - Create rich, customizable static reports for increased visibility into tasks.
* - {doc}`🏎 Optimizing Tasks <optimizing_tasks>`
  - Make tasks scalable, performant, and robust to unexpected failures.
* - {doc}`🔌 Extending Flyte <extending_flyte>`
  - Customize Flyte types and tasks to fit your needs.
```

```{admonition} Learn more
:class: important

For a comprehensive view of all of Flyte's functionality, see the
{ref}`User Guide <userguide>`, and to learn how to deploy a production Flyte
cluster, see the {ref}`Deployment Guide <deployment>`.
```

```{toctree}
:maxdepth: -1
:hidden:

tasks_and_workflows
creating_flyte_project
package_register
run_schedule
visualizing_artifacts
optimizing_tasks
extending_flyte
```
