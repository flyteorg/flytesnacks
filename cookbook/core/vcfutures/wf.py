import os
import uuid

from algopipelines.flytedatapipeline.kubes import (
    slack_notify,
    parse_session_info,
    parse_takes_status,
    git_clone,
    should_run_fit,
    qt_texture_training,
    get_parameters,
    skip,
)

from algopipelines.flytedatapipeline.subworkflows.shape_fit_flow import shape_fit_flow
from algopipelines.flytedatapipeline.subworkflows.evaluation_flow import evaluation_flow
from flytekit import workflow, conditional

@workflow
def smplx_proccess_pipeline(dummy: bool):

    pipeline_params = get_parameters(dummy=dummy)
    parsed_session_info = parse_session_info(dummy=dummy)
    parsed_takes_status = parse_takes_status(dummy=dummy)

    slack_notify(dummy=dummy)

    run_fit = should_run_fit(dummy=dummy)

    (motion_capture_repo := git_clone(dummy=dummy).with_overrides(name="Clone CGMocap")) >> run_fit
    (core_algo_repo := git_clone(dummy=dummy).with_overrides(name="Clone CoreAlgo")) >> run_fit
    (evaluator_repo := git_clone(dummy=dummy).with_overrides(name="Clone Evaluators")) >> run_fit
    (fitting_repo := git_clone(dummy=dummy).with_overrides(name="Clone Fitting")) >> run_fit
    (common_algo_repo := git_clone(dummy=dummy).with_overrides(name="Clone CommonAlgo")) >> run_fit

    conditional_fit = conditional("dummy_condition_1").if_(run_fit.is_true()
    ).then(shape_fit_flow(
        dummy=dummy
    )).else_().then(skip())

    conditional_train_qt = conditional("should_train_qt").if_(dummy == True
    ).then(qt_texture_training(
        dummy=dummy
    )).else_().then(skip())

    conditional_evaluation = conditional("should_run_evaluation").if_(dummy == True
    ).then(evaluation_flow(
        dummy=dummy
    )).else_().then(skip())


    # Dependencies that were handled by flyte before dummying the workflow:

    # git_clone nodes are inputs of all of the conditionals
    # parsed_session_info is an input of all the conditionals
    # parsed_takes_status is an input of the evaluation conditional
    # pipeline_params is an input of all the conditionals

    # Explicit dependencies related to our specific logic:

    pipeline_params >> run_fit

    motion_capture_repo >> conditional_train_qt
    core_algo_repo >> conditional_train_qt
    common_algo_repo >> conditional_train_qt
    evaluator_repo >> conditional_train_qt
    fitting_repo >> conditional_train_qt

    conditional_fit >> conditional_train_qt
    conditional_fit >> parsed_takes_status
    conditional_train_qt >> conditional_evaluation
