#!/bin/bash

#set -e
FLYTESNACKS_VERSION=$(curl --silent "https://api.github.com/repos/flyteorg/flytesnacks/releases/latest" | jq -r .tag_name)
for row in $(cat cookbook/flyte_tests_manifest.json | jq -c '.[]'); do
  flytectl register file "https://github.com/flyteorg/flytesnacks/releases/download/${FLYTESNACKS_VERSION}/flytesnacks-$(echo ${row} | jq -r '.name').tgz"  -d development  -p flytesnacks --archive --config ~/.flyte/config-sandbox.yaml
done
