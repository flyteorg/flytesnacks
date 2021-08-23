# Run the Workflow in a Sandbox Cluster

To run Flyte workflow in a sandbox cluster, Docker needs to be set up. Katacoda takes care of setting up the environment, so you can proceed with instantiating the Flyte-related libaries. 

## Flytectl

Since flytectl is already installed as part of the environment setup, you can directly initialize flytectl. Flytectl is a commandline interface for Flyte. Refer to the [Flytectl docs](https://docs.flyte.org/projects/flytectl/en/stable/) to know more about it.
`flytectl config init`{{execute HOST1}}

Next, start the sandbox.
`flytectl sandbox start --source=../ml_training`{{execute HOST1}}

## Build & Deploy the Application to Cluster

Flyte uses Docker containers to package the workflows and tasks and sends them to the remote Flyte cluster. Thus, there is a Dockerfile already included in the cloned repo. You can combine the build and push step by simply building the image inside the Flyte-sandbox container. This can be done using the following command:
`flytectl sandbox exec -- docker build . --tag "myapp:v1" -f pima_diabetes/Dockerfile`{{execute HOST1}}

Next, package the workflow using the pyflyte cli bundled with Flytekit and upload it to the Flyte backend. Note that the image is the same as the one built in the previous step.
`pyflyte --pkgs pima_diabetes package --image myapp:v1 --force --output=flyte.tgz `{{execute HOST1}}

Upload this package to the Flyte backend. We call this "registration".
`flytectl register files --archive -p flytesnacks -d development flyte.tgz --version=v1`{{execute HOST1}}

Finally, visualize the registered workflow.
`flytectl get workflow pima_diabetes.diabetes.diabetes_xgboost_model -p flytesnacks -d development --latest -o doturl`{{execute HOST1}}

## Execute on Flyte Cluster

Launch the workflow from CLI using Flytectl.

1. Generate an execution spec file
`flytectl get launchplan --project flytesnacks --domain development pima_diabetes.diabetes.diabetes_xgboost_model --latest --execFile exec_spec.yaml`{{execute HOST1}}

2. Open `ml_training/exec_spec.yaml`{{open}} and change the value of input

3. Create an execution using the exec spec file
`flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml`{{execute HOST1}}

4. Visit the Flyte console at https://[[HOST_SUBDOMAIN]]-30081-[[KATACODA_HOST]].environments.katacoda.com/console to view and monitor the workflow


You have successfully packaged your workflow and tasks and pushed them to Flyte cluster. Next, let's dive into iteration.
