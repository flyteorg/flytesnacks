# %% [markdown]
# (imperative_workflow)=
#
# # Imperative Workflows
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Workflows are commonly created by applying the `@workflow` decorator to Python functions.
# During compilation, this involves processing the function's body and utilizing subsequent calls to
# underlying tasks to establish and record the workflow structure. This approach is known as declarative
# and is suitable when manually drafting the workflow.
#
# However, in cases where workflows are constructed programmatically, an imperative style is more appropriate.
# For instance, if tasks have been defined already, their sequence and dependencies might have been specified
# in textual form (perhaps during a transition from a legacy system).
# In such scenarios, you want to orchestrate these tasks.
# This is where Flyte's imperative workflows come into play, allowing you to programmatically construct workflows.
#
# To begin, import the necessary dependencies.
# %%
from flytekit import Workflow


# %% [markdown]
# We import the `slope` and `intercept` tasks from the `workflow.py` file.
# %%
from .workflow import slope, intercept

# %% [markdown]
# Create an imperative workflow.
# %%
imperative_wf = Workflow(name="imperative_workflow")

# %% [markdown]
# Add the workflow inputs to the imperative workflow.
# %%
imperative_wf.add_workflow_input("x", list[str])
imperative_wf.add_workflow_input("y", list[str])

# %% [markdown]
# ::: {note}
# If you want to assign default values to the workflow inputs,
# you can create a {ref}`launch plan <launch_plan>`.
# :::
#
# Add the tasks that need to be triggered from within the workflow.
# %%
node_t1 = imperative_wf.add_entity(slope, x=imperative_wf.inputs["x"])
node_t2 = imperative_wf.add_entity(intercept, y=node_t1.outputs["o0"])

# %% [markdown]
# Lastly, add the workflow output.
# %%
imperative_wf.add_workflow_output("wf_output", node_t2.outputs["o0"])

# %% [markdown]
# You can execute the workflow locally as follows:
# %%
if __name__ == "__main__":
    print(f"Running imperative_wf() {imperative_wf(x=[-3, 0, 3], y=[7, 4, -2])}")

# %% [markdown]
# :::{note}
# You also have the option to provide a list of inputs and
# retrieve a list of outputs from the workflow.
#
# ```python
# wf_input_y = imperative_wf.add_workflow_input("y", list[str])
# node_t3 = wf.add_entity(some_task, a=[wf.inputs["x"], wf_input_y])
# ```
#
# ```python
# wf.add_workflow_output(
#     "list_of_outputs",
#     [node_t1.outputs["o0"], node_t2.outputs["o0"]],
#     python_type=list[str],
# )
# ```
# :::
