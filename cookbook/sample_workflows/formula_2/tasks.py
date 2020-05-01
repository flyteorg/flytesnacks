from __future__ import absolute_import
from __future__ import print_function

from flytekit.sdk.tasks import inputs, outputs, python_task
from flytekit.sdk.types import Types


@inputs(num=Types.Integer)
@outputs(out=Types.Integer)
@python_task
def inner_task(wf_params, num, out):
    wf_params.logging.info("Running inner task... setting output to input")
    out.set(num)


@inputs(num=Types.Integer)
@outputs(out=Types.Integer)
@python_task
def inverse_inner_task(wf_params, num, out):
    wf_params.logging.info("Running inner task... setting output to input")
    out.set(-num)
