## Fast Register 

### Fast serialize package 
` pyflyte --pkgs pima_diabetes  package --image myapp:v1 --source=.  --force --output=flyte.tgz --fast`{{execute HOST1}}

### Register Serialize example
`flytectl register files --archive -p flytesnacks -d development flyte.tgz --version=v2`{{execute HOST1}}

### Get workflow
`flytectl get workflow pima_diabetes.diabetes.diabetes_xgboost_model -p flytesnacks -d development  --latest -o doturl`{{execute HOST1}}

### Get launchplan 
`flytectl get launchplan --project flytesnacks --domain development pima_diabetes.diabetes.diabetes_xgboost_model  --latest --execFile exec_spec.yaml`{{execute HOST1}}

### Create Launchplan
`flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml`{{execute HOST1}}

Please check tutorials for writing [your tasks ](https://lyft.github.io/flyte/user/getting_started/create_first.html)