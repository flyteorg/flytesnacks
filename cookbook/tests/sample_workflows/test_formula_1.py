

from cookbook.sample_workflows.formula_1 import dynamic as _dynamic

from flytekit.configuration import set_flyte_config_file

set_flyte_config_file('/Users/ytong/go/src/github.com/lyft/flyteexamples')


def test_build():
    result = _dynamic.workflow_builder.unit_test(task_input_num=3, decider=True)
    print(result)
