#!/bin/bash

set -e

for row in $(cat flyte_tests_manifest.json | jq -c '.[]'); do
  tar -cvzf "./release-snacks/flytesnacks-$(echo ${row} | jq -r '.name').tgz"  "./$(echo ${row} | jq -r '.path')/_pb_output/"
done