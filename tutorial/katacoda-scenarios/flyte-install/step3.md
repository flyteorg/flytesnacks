# Build & Deploy Your Application “Fast”er!

Let's now understand how to register workflows when code changes are made.

For illustration purposes, do a trivial code change in the code. Remove `test_split_ratio` as the workflow parameter and send it as a hard-coded argument.

```
@workflow
def diabetes_xgboost_model(
    dataset: FlyteFile[
        typing.TypeVar("csv")
    ] = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv",
    seed: int = 7,
) -> workflow_outputs:
    """
    This pipeline trains an XGBoost mode for any given dataset that matches the schema as specified in
    https://github.com/jbrownlee/Datasets/blob/master/pima-indians-diabetes.names.
    """
    x_train, x_test, y_train, y_test = split_traintest_dataset(
        dataset=dataset, seed=seed, test_split_ratio=0.33
    )
    model = fit(x=x_train, y=y_train, hyperparams=XGBoostModelHyperparams(max_depth=4),)
    predictions = predict(x=x_test, model_ser=model.model)
    return model.model, score(predictions=predictions, y=y_test)
```

Package the workflow using the following command:
`pyflyte --pkgs pima_diabetes package --image myapp:v1 --force --output=flyte.tgz --fast`{{execute HOST1}}

Note: `--fast` flag will take the code from your local machine and provide it for execution without having to build the container and push it. This is called "fast registration".

Now, fast-register the example:
`flytectl register files --archive -p flytesnacks -d development flyte.tgz --version=v1-fast`{{execute HOST1}}

Visualize the registered workflow.
`flytectl get workflow pima_diabetes.diabetes.diabetes_xgboost_model -p flytesnacks -d development  --latest -o doturl`{{execute HOST1}}

## Execute on Flyte Cluster

1. Generate an execution spec file
`flytectl get launchplan --project flytesnacks --domain development pima_diabetes.diabetes.diabetes_xgboost_model  --latest --execFile exec_spec.yaml`{{execute HOST1}}

2. Create an execution using the exec spec file
`flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml`{{execute HOST1}}

3. Visit the Flyte console at https://[[HOST_SUBDOMAIN]]-30081-[[KATACODA_HOST]].environments.katacoda.com/console to view and monitor the workflow

🎉 Congratulations! You have now:

- Run a Flyte workflow locally,
- Started a Flyte sandbox cluster,
- Run a Flyte workflow on a cluster,
- Iterated on a Flyte workflow.

To experience the full capabilities of Flyte, take a look at the [User Guide](https://docs.flyte.org/projects/cookbook/en/latest/user_guide.html).