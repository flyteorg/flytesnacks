# Using Sagemaker with Flyte - Sagemaker plugin

## Prerequisites
Before following this example, make sure that 
- SageMaker plugins are [enabled in flytepropeller's config](https://github.com/lyft/flytepropeller/blob/f9819ab2f4ff817ce5f8b8bb55a837cf0aeaf229/config.yaml#L35-L36)
- [AWS SageMaker k8s operator](https://github.com/aws/amazon-sagemaker-operator-for-k8s) is installed in your k8s cluster


## Define a Training Job Task of SageMaker's built-in algorithm

Define a training job of SageMaker's built-in algorithm using Flytekit's `SdkBuiltinAlgorithmTrainingJobTask`:

```python
from flytekit.models.sagemaker import training_job as training_job_models
from flytekit.common.tasks.sagemaker import training_job_task

alg_spec = training_job_models.AlgorithmSpecification(
    input_mode=training_job_models.InputMode.FILE,
    algorithm_name=training_job_models.AlgorithmName.XGBOOST,
    algorithm_version="0.72",
    input_content_type=training_job_models.InputContentType.TEXT_CSV,
)

xgboost_train_task = training_job_task.SdkBuiltinAlgorithmTrainingJobTask(
    training_job_resource_config=training_job_models.TrainingJobResourceConfig(
        instance_type="ml.m4.xlarge",
        instance_count=1,
        volume_size_in_gb=25,
    ),
    algorithm_specification=alg_spec,
    cache_version='1',
    cacheable=True,
)
```
## Launch a Training Job Task
You can launch the training job standalone or from within a workflow.

```python
# Launching the training job standalone

xgboost_hyperparameters = {
    "num_round": "100",  # num_round is a required hyperparameter for XGBoost
    "base_score": "0.5",  
    "booster": "gbtree",  
}

training_inputs={
    "train": "s3://path/to/your/train/data/csv/folder",
    "validation": "s3://path/to/your/validation/data/csv/folder",
    "static_hyperparameters": xgboost_hyperparameters,
}

# Invoking the SdkBuiltinAlgorithmTrainingJobTask
training_exc = xgboost_train_task.register_and_launch("project", "domain", inputs=training_inputs)


# Invoking the training job from within a workflow

@workflow_class()
class TrainingWorkflow(object):
    ... 
    # The following two lines are just for demonstration purpose
    train_data = get_train_data(...)    
    validation_data = get_validation_data(...)

    # Invoking the training job 
    train = xgboost_train_task(
        train=train_data.outputs.output_csv,
        validation=validation_data.outputs.output_csv,
        static_hyperparameters=xgboost_hyperparameters,
    )

    ...
```

## Define hyperparameter tuning job 

### Wrapping a SageMaker Hyperparameter Tuning Job around a SageMaker Training Job

Define the hyperparameter tuning job, which is required to wrap around a training job:

```python
from flytekit.common.tasks.sagemaker import hpo_job_task
xgboost_hpo_task = hpo_job_task.SdkSimpleHyperparameterTuningJobTask(
    training_job=xgboost_train_task,
    max_number_of_training_jobs=10,
    max_parallel_training_jobs=5,
    cache_version='1',
    retries=2,
    cacheable=True,
)
```

### Invoking the hyperparameter tuning job using single-task execution
```python
from flytekit.models.sagemaker.hpo_job import HyperparameterTuningJobConfig, \
    HyperparameterTuningObjectiveType, HyperparameterTuningStrategy, \
    TrainingJobEarlyStoppingType, HyperparameterTuningObjective
from flytekit.models.sagemaker.parameter_ranges import HyperparameterScalingType, \ 
    ParameterRanges, ContinuousParameterRange, IntegerParameterRange

hpo_inputs={
    "train": "s3://path/to/your/train/data/csv/folder",
    "validation": "s3://path/to/your/validation/data/csv/folder",
    "static_hyperparameters": xgboost_hyperparameters,
    "hyperparameter_tuning_job_config": HyperparameterTuningJobConfig(
        hyperparameter_ranges=ParameterRanges(
            parameter_range_map={
                "num_round": IntegerParameterRange(min_value=3, max_value=10, 
                                                   scaling_type=HyperparameterScalingType.LINEAR),
                "gamma": ContinuousParameterRange(min_value=0.0, max_value=0.3,
                                                  scaling_type=HyperparameterScalingType.LINEAR),
            }
        ),
        tuning_strategy=HyperparameterTuningStrategy.BAYESIAN,
        tuning_objective=HyperparameterTuningObjective(
            objective_type=HyperparameterTuningObjectiveType.MINIMIZE,
            metric_name="validation:error",
        ),
        training_job_early_stopping_type=TrainingJobEarlyStoppingType.AUTO
    ).to_flyte_idl(),
}

hpo_exc = xgboost_hpo_task.register_and_launch("flyteexamples", "development", inputs=hpo_inputs)
```

### Invoking the hyperparameter tuning job from a workflow.

```python
from flytekit.models.sagemaker.hpo_job import HyperparameterTuningJobConfig, \
    HyperparameterTuningObjectiveType, HyperparameterTuningStrategy, \
    TrainingJobEarlyStoppingType, HyperparameterTuningObjective
from flytekit.models.sagemaker.parameter_ranges import HyperparameterScalingType, \ 
    ParameterRanges, ContinuousParameterRange, IntegerParameterRange

@workflow_class()
class TrainingWorkflow(object):    
    # Retrieve data
    train_data = get_train_data(...)
    validation_data = get_validation_data(...)

    train = xgboost_hpo_task(
        # Using the input we got from the Presto tasks
        train=train_data.outputs.output_csv,
        validation=validation_data.outputs.output_csv,
        
        static_hyperparameters=xgboost_hyperparameters,
        hyperparameter_tuning_job_config=HyperparameterTuningJobConfig(    
            hyperparameter_ranges=ParameterRanges(
                parameter_range_map={
                    "num_round": IntegerParameterRange(min_value=3, max_value=10, 
                                                       scaling_type=HyperparameterScalingType.LINEAR),
                    "max_depth": IntegerParameterRange(min_value=5, max_value=7, 
                                                       scaling_type=HyperparameterScalingType.LINEAR),
                    "gamma": ContinuousParameterRange(min_value=0.0, max_value=0.3,
                                                      scaling_type=HyperparameterScalingType.LINEAR),
                }
            ),
            tuning_strategy=HyperparameterTuningStrategy.BAYESIAN,
            tuning_objective=HyperparameterTuningObjective(
                objective_type=HyperparameterTuningObjectiveType.MINIMIZE,
                metric_name="validation:error",
            ),
            training_job_early_stopping_type=TrainingJobEarlyStoppingType.AUTO
        ).to_flyte_idl(),
    )
```
