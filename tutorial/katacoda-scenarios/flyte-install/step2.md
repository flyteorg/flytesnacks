## Setup Sandbox 


### Setup flytectl config
`flytectl config init`{{execute HOST1}}

### Start Sandbox 
`flytectl sandbox start --source=./ml_training`{{execute HOST1}}

### Setup example
`pip install flytekit`{{execute HOST1}}
`cd ml_training/pima_diabetes`{{execute HOST1}}
`pip install -r requirements.txt`{{execute HOST1}}
`cd ../`{{execute HOST1}}


### Build docker image for 
`flytectl sandbox exec -- docker build . --tag "myapp:v1" -f pima_diabetes/Dockerfile`{{execute HOST1}}

### Serialize package
`pyflyte --pkgs pima_diabetes  package --image myapp:v1 --source=pima_diabetes/..  --force --output=flyte.tgz `{{execute HOST1}}

### Register Serialize example
`flytectl register files --archive -p flytesnacks -d development flyte.tgz --version=v1`{{execute HOST1}}

### Get workflow
`flytectl get workflow pima_diabetes.diabetes.diabetes_xgboost_model -p flytesnacks -d development  --latest -o doturl`{{execute HOST1}}

### Get launchplan 
`flytectl get launchplan --project flytesnacks --domain development pima_diabetes.diabetes.diabetes_xgboost_model  --latest --execFile exec_spec.yaml`{{execute HOST1}}

### Create Launchplan
`flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml`{{execute HOST1}}

You can check workflow execution in flyteconsole 

After this visit flyte console https://[[HOST_SUBDOMAIN]]-30081-[[KATACODA_HOST]].environments.katacoda.com/console


