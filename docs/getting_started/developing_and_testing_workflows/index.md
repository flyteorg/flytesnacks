---
# override the toc-determined page navigation order
prev-page: getting_started/running_a_workflow_locally
prev-page-title: Running a workflow locally
---

(developing_and_testing_workflows)=
# Developing and testing workflows

In this section we will guide you through the Flyte workflow development process.

As with all software development, the process is an iterative cycle of writing, testing, running and debugging your code.

The difference with Flyte is that any point in the cycle you have a choice of three different ways of running your code:

* In your local Python environment
* On a local cluster
* On a remote cluster

This allows you to test your code in progressively more production-realistic environments as you develop it.

This section will walk you through how to set up your environment to enable each of these modes of execution and how to the Flyte development tools to actually run your code in each.

```{toctree}
:maxdepth: -1
:hidden:

writing_your_code
setting_up_your_image
registering_and_running_workflows_on_a_flyte_cluster
scheduling_workflows_with_launch_plans
scripting_workflow_and_launch_plan_execution_with_flyteremote
creating_a_flyte_project_on_a_cluster
using_secrets_in_flyte_tasks
using_flyte_agents
mocking_tasks
integration_testing
inspecting_and_debugging_workflow_and_task_executions
```
