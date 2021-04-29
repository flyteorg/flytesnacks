"""
Training builtin algorithms on Amazon Sagemaker
###################################################
In this example we will show how it is possible to work with Built-in algorithms with Amazon sagemaker and even
perform Hyper parameter optimization using Sagemaker HPO


Defining a XGBoost Training job
--------------------------------
We will create a job that will train an XGBoost model using the prebuilt algorithms @Sagemaker.
Refer to `Sagemaker XGBoost docs here <https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html>`_
To understand more about XGBoost refer `here <https://xgboost.readthedocs.io/en/latest/>`_.
To dive deeper into the Flytekit API refer to
`docs <https://lyft.github.io/flyte/flytekit/flytekit.common.tasks.sagemaker.html?highlight=sagemaker#module-flytekit.common.tasks.sagemaker>`_
"""
import typing

from flytekit import TaskMetadata
from flytekitplugins.awssagemaker import (
    AlgorithmName,
    AlgorithmSpecification,
    ContinuousParameterRange,
    HPOJob,
    HyperparameterScalingType,
    HyperparameterTuningJobConfig,
    HyperparameterTuningObjective,
    HyperparameterTuningObjectiveType,
    HyperparameterTuningStrategy,
    InputContentType,
    InputMode,
    IntegerParameterRange,
    ParameterRangeOneOf,
    SagemakerBuiltinAlgorithmsTask,
    SagemakerHPOTask,
    SagemakerTrainingJobConfig,
    TrainingJobEarlyStoppingType,
    TrainingJobResourceConfig,
)

# %%
# Defining the values of some hyperparameters, which will be used by the TrainingJob
# these hyper-parameters are commonly used by the XGboost algorithm. Here we bootstrap them with some default Values
# Usually the default values are selected or "tuned - refer to next section"
xgboost_hyperparameters: typing.Dict[str, str] = {
    "num_round": "100",
    "base_score": "0.5",
    "booster": "gbtree",
    "csv_weights": "0",
    "dsplit": "row",
    "grow_policy": "depthwise",
    "lambda_bias": "0.0",
    "max_bin": "256",
    "normalize_type": "tree",
    "objective": "reg:linear",
    "one_drop": "0",
    "prob_buffer_row": "1.0",
    "process_type": "default",
    "refresh_leaf": "1",
    "sample_type": "uniform",
    "scale_pos_weight": "1.0",
    "silent": "0",
    "skip_drop": "0.0",
    "tree_method": "auto",
    "tweedie_variance_power": "1.5",
    "updater": "grow_colmaker,prune",
}

# %%
# Here we define the actual algorithm (XGBOOST) and version of the algorithm to use
alg_spec = AlgorithmSpecification(
    input_mode=InputMode.FILE,
    algorithm_name=AlgorithmName.XGBOOST,
    algorithm_version="0.90",
    input_content_type=InputContentType.TEXT_CSV,
)

# %%
# Finally lets use Flytekit plugin called SdkBuiltinAlgorithmTrainingJobTask, to create a task that wraps the algorithm.
# This task does not really have a user-defined function as the actual algorithm is pre-defined in Sagemaker.
# But, this task still has the same set of properties like any other FlyteTask
# - Caching
# - Resource specification
# - versioning etc
xgboost_train_task = SagemakerBuiltinAlgorithmsTask(
    name="xgboost_trainer",
    task_config=SagemakerTrainingJobConfig(
        algorithm_specification=alg_spec,
        training_job_resource_config=TrainingJobResourceConfig(
            instance_type="ml.m4.xlarge", instance_count=1, volume_size_in_gb=25,
        ),
    ),
    metadata=TaskMetadata(cache_version="1.0", cache=True),
)


# %%
# You can use
# `Single task Execution <https://lyft.github.io/flyte/user/features/single_task_execution.html?highlight=single%20task%20execution>`_
# to execute just the task without needing to create a workflow.  To trigger an execution, you need to provide
#
# Project (flyteexamples) project where the execution will be created under
# Domain (development) domain where the execution will be created, under the project
# inputs - the actual inputs
#
# Pre-built algorithms have restrictive set of inputs. They always expect
#
# #. Training data set
# #. Validation data set
# #. Static set of hyper parameters as a dictionary
#
# In this case we have taken the `PIMA Diabetes dataset <https://www.kaggle.com/kumargh/pimaindiansdiabetescsv>`_
# and split it and uploaded to an s3 bucket
def execute_training():
    xgboost_train_task(
        static_hyperparameters=xgboost_hyperparameters, train="", validation="",
    )


# %%
#
# Optimize the hyper-parameters
# --------------------------------
# Amazon Sagemaker offers automatic hyper parameter blackbox optimization using HPO Service.
# This technique is highly effective to figure out the right set of hyper parameters to use that
# improve the overall accuracy of the model (or minimize the error)
# Flyte makes it extremely effective to optimize a model using Amazon Sagemaker HPO. In this example we will look how
# this can be done for the prebuilt algorithm training done in the previous section
#
# Define an HPO Task, that wraps the training task
# -------------------------------------------------
# So to start with hyper parameter optimization, once a training task is created, wrap it in
# SagemakerHPOTask as follows
#


xgboost_hpo_task = SagemakerHPOTask(
    name="xgboost_hpo",
    task_config=HPOJob(
        max_number_of_training_jobs=10,
        max_parallel_training_jobs=5,
        tunable_params=["num_round", "max_depth", "gamma"],
    ),
    training_task=xgboost_train_task,
    metadata=TaskMetadata(cache=True, cache_version="1.0", retries=2),
)


# %%
# Launch the HPO Job
# -------------------
# Just like Training Job, HPO job can be launched directly from the notebook The inputs for an HPO job that wraps a
# training job, are the combination of all inputs for the training job - i.e,
#
# #. "train" dataset, "validation" dataset and "static hyper parameters" for Training job
# #. HyperparameterTuningJobConfig, which consists of ParameterRanges, for the parameters that should be tuned,
# #. tuning strategy - Bayesian OR Random (or others as described in Sagemaker)
# #. Stopping condition and
# #. Objective metric name and type (whether to minimize etc)
#
# When launching the TrainingJob and HPOJob, we need to define the inputs.
# Inputs are those directly related to algorithm outputs. We use the inputs
# and the version information to decide cache hit/miss
def execute():
    # TODO Local execution of hpo task is not supported. To add example of remote execution
    xgboost_hpo_task(
        # These 3 parameters are implicitly extracted from the training task itself
        static_hyperparameters=xgboost_hyperparameters,
        train="s3://demo/test-datasets/pima/train",
        validation="s3://demo/test-datasets/pima/validation",
        # The following parameteres are specific for hyper parameter tuning and allow to modify tuning at launch time
        hyperparameter_tuning_job_config=HyperparameterTuningJobConfig(
            tuning_strategy=HyperparameterTuningStrategy.BAYESIAN,
            tuning_objective=HyperparameterTuningObjective(
                objective_type=HyperparameterTuningObjectiveType.MINIMIZE,
                metric_name="validation:error",
            ),
            training_job_early_stopping_type=TrainingJobEarlyStoppingType.AUTO,
        ),
        # The following parameters are tunable parameters are specified during the configuration of the task
        # this section provides the ranges to be sweeped
        num_round=ParameterRangeOneOf(
            param=IntegerParameterRange(
                min_value=3, max_value=10, scaling_type=HyperparameterScalingType.LINEAR
            )
        ),
        max_depth=ParameterRangeOneOf(
            param=IntegerParameterRange(
                min_value=5, max_value=7, scaling_type=HyperparameterScalingType.LINEAR
            )
        ),
        gamma=ParameterRangeOneOf(
            param=ContinuousParameterRange(
                min_value=0.0,
                max_value=0.3,
                scaling_type=HyperparameterScalingType.LINEAR,
            )
        ),
    )


# %%
# Register and launch the task standalone!
# hpo_exc = xgboost_hpo_task.register_and_launch("flyteexamples", "development", inputs=hpo_inputs)
