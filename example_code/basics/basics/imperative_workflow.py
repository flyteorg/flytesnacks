from flytekit import Workflow

# Import the `slope` and `intercept` tasks from the workflow.py file
from .workflow import intercept, slope

# Create an imperative workflow
imperative_wf = Workflow(name="imperative_workflow")


# Add the workflow inputs to the imperative workflow
imperative_wf.add_workflow_input("x", list[int])
imperative_wf.add_workflow_input("y", list[int])


# Add the tasks that need to be triggered from within the workflow
node_t1 = imperative_wf.add_entity(slope, x=imperative_wf.inputs["x"], y=imperative_wf.inputs["y"])
node_t2 = imperative_wf.add_entity(
    intercept, x=imperative_wf.inputs["x"], y=imperative_wf.inputs["y"], slope=node_t1.outputs["o0"]
)


# Add the workflow output
imperative_wf.add_workflow_output("wf_output", node_t2.outputs["o0"])


# Execute the workflow locally as follows
if __name__ == "__main__":
    print(f"Running imperative_wf() {imperative_wf(x=[-3, 0, 3], y=[7, 4, -2])}")
