#!/bin/bash

set -e

for row in $(cat flytetester.json | jq -c '.[]'); do
  echo "tar -zcvf ./release-snacks/flytesnacks-$(echo ${row} | jq -r '.name').tar.gz  ./$(echo ${row} | jq -r '.path')/_pb_output"
done