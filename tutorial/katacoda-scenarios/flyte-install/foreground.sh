curl https://storage.googleapis.com/kubernetes-release/release/v1.18.10/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl
chmod a+x /usr/local/bin/kubectl
curl -s https://raw.githubusercontent.com/flyteorg/flytectl/master/install.sh | bash
mv bin/flytectl /usr/local/bin/flytectl
chmod a+x /usr/local/bin/flytectl

git clone https://github.com/flyteorg/flytesnacks.git ~/tmp/flytesnacks
mv ~/tmp/flytesnacks/cookbook/case_studies/ml_training ~/