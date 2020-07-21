# Creating Launch Plans

Please first take a moment to review the [Launch Plans](https://docs.lyft.net/eng/flytedocs/user/concepts/launchplans_schedules.html#launch-plans) documentation.

In order to create a launch plan we first need a workflow. We can use the `IdentityWorkflow` created in one of the examples.

```python
from recipes.compose.inner import IdentityWorkflow
```

A default launch plan can be created by just calling the `.create_launch_plan()` function on the Workflow with no arguments.
```python
IdentityWorkflow.create_launch_plan()
```

```python
from flytekit.sdk.types import Types
with_default = IdentityWorkflow.create_launch_plan(
    default_inputs={'a': Input(Types.Integer, default=1)}
)
```