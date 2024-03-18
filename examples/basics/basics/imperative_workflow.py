from flytekit import Workflow
from .workflow import intercept, slope


imperative_wf = Workflow(name="imperative_workflow")
imperative_wf.add_workflow_input("x", list[int])
imperative_wf.add_workflow_input("y", list[int])

node_t1 = imperative_wf.add_entity(slope, x=imperative_wf.inputs["x"], y=imperative_wf.inputs["y"])
node_t2 = imperative_wf.add_entity(
    intercept, x=imperative_wf.inputs["x"], y=imperative_wf.inputs["y"], slope=node_t1.outputs["o0"]
)

imperative_wf.add_workflow_output("wf_output", node_t2.outputs["o0"])

if __name__ == "__main__":
    print(f"Running imperative_wf() {imperative_wf(x=[-3, 0, 3], y=[7, 4, -2])}")
