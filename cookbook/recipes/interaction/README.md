# Interactive development and debugging with Flyte

In this recipe we will talk about how to interact with an existing Workflow or execution. This is not a tutorial for developing a Workflow interactively.

Alright, so we have a workflow or a task that is already registered. A registered workflow/task refers to those that were passed to register workflow or task. FlyteAdmin is aware of the name of the
Workflow or task and they can be retrieved using flyte-cli. So before get get started with the following steps, lets register workflows and tasks in this directory.

## Part 0: Execute tasks locally
The method `unit_test` is implicitly defined on a Flyte task. This can be invoked from any interactive or programmatic medium.
It is useful in writing programmatic unit tests

### Jupyter Notebook
[Exhibit: part_0.ipynb](part_0.ipynb)

## Part 1: Executing a Pre-registered task
Once the registration is successful, task executions can be independently launched

### Jupyter Notebook
[Exhibit: part_1.ipynb](part_1.ipynb)

### CLI (flyte-cli)
```bash
 $ flyte-cli -h localhost:30081 -i list-task-versions -p flytesnacks -d development --name recipes.interaction.interaction.scale
 # Get the URN
 $ flyte-cli -h localhost:30081 -i launch-task -p flytesnacks -d development -u <urn> -- image=https://miro.medium.com/max/1400/1*qL8UYfaStcEo_YVPrA4cbA.png
```

### Console
**Not yet supported**

*Currently launching a task from the console is not Supported*


## Part 2:  Executing a Pre-registered Workflow / LaunchPlan

### Jupyter Notebook
[Exhibit: part_1.ipynb](part_1.ipynb)

### CLI (flyte-cli)
```bash

```

### Console
1. Navigate to **Console Homepage > Flyte Examples | development > recipes.interaction.interaction.FailingWorkflow**
    - If Using console on localhost sandbox (docker for mac mostly then)
      [Workflow Link](http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/recipes.interaction.interaction.FailingWorkflow)
2. Click on the Launch Button

## Part 3: Retrieving outputs of error from a previous execution

### Jupyter Notebook
[Exhibit: part_1.ipynb](part_1.ipynb)

### CLI (flyte-cli)
```bash

```

### Console
1. Navigate to **Console Homepage > Flyte Examples | development > recipes.interaction.interaction.FailingWorkflow**
    - If Using console on localhost sandbox (docker for mac mostly then)
      [Workflow Link](http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/recipes.interaction.interaction.FailingWorkflow)
2. Click on the Launch Button

## Part 4: Relaunching a failed execution

### Jupyter Notebook
[Exhibit: part_1.ipynb](part_1.ipynb)

### CLI (flyte-cli)
```bash

```

### Console
1. Navigate to **Console Homepage > Flyte Examples | development > recipes.interaction.interaction.FailingWorkflow**
    - If Using console on localhost sandbox (docker for mac mostly then)
      [Workflow Link](http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/recipes.interaction.interaction.FailingWorkflow)
2. Click on the Launch Button

## Part 5: Launch a new execution using partial outputs of a previous execution
