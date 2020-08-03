# Using Sagemaker with Flyte - Sagemaker plugin

## Prerequisites
Before following this example, make sure that 
- SageMaker plugins are [enabled in flytepropeller's config](https://github.com/lyft/flytepropeller/blob/f9819ab2f4ff817ce5f8b8bb55a837cf0aeaf229/config.yaml#L35-L36)
- [AWS SageMaker k8s operator](https://github.com/aws/amazon-sagemaker-operator-for-k8s) is installed in your k8s cluster

## How do I write a SageMaker task? 
### Launch a SageMaker Training Job with SageMaker's Built-in Algorithms

Define a training job of SageMaker's built-in algorithm using Flytekit's `SdkBuiltinAlgorithmTrainingJobTask`:

```python
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
    cache_version='blah9',
    cacheable=True,
)
```

And then launch the training job standalone or from within a workflow.
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