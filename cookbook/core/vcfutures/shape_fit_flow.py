import os
import uuid

from algopipelines.flytedatapipeline.kubes import (
    download_video_folder,
    mocap_shape_process,
    upload_folder,
    upload_status_file,
    skip,
)
from algopipelines.flytedatapipeline.data_pipelines.fitting_scripts.smplx_shape_fitting import smplx_shape_fitting
from algopipelines.flytedatapipeline.data_pipelines.fitting_scripts.smplx_expression_fitting import smplx_expression_fitting
from algopipelines.flytedatapipeline.subworkflows.mocap_process_flow import mocap_process_flow

from algopipelines.datahandler.k8s import task_config
from flytekit import conditional, dynamic
from flytekit.types.directory import FlyteDirectory



@dynamic(**task_config(
    image='algopipelines-generic:v1',
    cpu='400m', memory='400Mi'))
def shape_fit_flow(
    dummy=bool
):

    shape_video = download_video_folder(dummy=dummy)

    shape_fitting_outputs_qt = smplx_shape_fitting(dummy=dummy)
    upload_folder(dummy=dummy).with_overrides(name='Upload Shape Fitting Outputs')

    shape_fitting_outputs_lite = smplx_shape_fitting(dummy=dummy)
    upload_folder(dummy=dummy).with_overrides(name='Upload Shape Fitting Outputs (Lite)')

    mocap_shape_process_outputs = mocap_shape_process(dummy=dummy)

    upload_folder(dummy=dummy).with_overrides(name='Upload Mocap Shape Process Outputs')

    upload_folder(dummy=dummy).with_overrides(name='Upload Shape Raw Data')

    for expression_path in ['dummy_path_1', "dummy_path_2", "...", "dummy_path_13"]:

        expression_video = download_video_folder(dummy=dummy)

        upload_folder(dummy=dummy).with_overrides(name="Upload Expression Raw Data")

        expression_fitting_outputs = smplx_expression_fitting(dummy=dummy)

        upload_status_file(dummy=dummy)

        upload_folder(dummy=dummy)

        conditional("should_run_mocap_processing").if_("dummy" == "dummy").then(
            mocap_process_flow(dummy-dummy)
        ).else_().then(skip())
