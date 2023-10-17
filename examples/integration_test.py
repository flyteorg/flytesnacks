from basics.basics.documenting_workflows import google_docstring_wf, numpy_docstring_wf, sphinx_docstring_wf
from basics.basics.hello_world import hello_world_wf
from basics.basics.imperative_workflow import imperative_wf
from basics.basics.launch_plan import simple_wf_lp_fixed_inputs
from basics.basics.named_outputs import simple_wf_with_named_outputs
from basics.basics.shell_task import shell_task_wf
from basics.basics.task import slope
from basics.basics.workflow import simple_wf_with_partial
from ray_plugin.ray_plugin.ray_example import ray_workflow
from flytekit import workflow, task


@workflow
def integration_test():
    # Test Basic Workflows
    google_docstring_wf()
    numpy_docstring_wf()
    sphinx_docstring_wf()

    hello_world_wf()
    imperative_wf(x=[-3, 0, 3], y=[7, 4, -2])

    simple_wf_lp_fixed_inputs(y=[-3, 2, -2])
    simple_wf_with_named_outputs()

    shell_task_wf()
    slope(x=[-3, 0, 3], y=[7, 4, -2])
    simple_wf_with_partial(x=[-3, 0, 3], y=[7, 4, -2])

    # Test Plugins
    ray_workflow(n=5)

    # TODO: Add more plugins here, like spark, tensorflow, torch, Dask.


if __name__ == '__main__':
    integration_test()
