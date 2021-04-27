#!/bin/bash

set -e

tar -zcvf ./release-snacks/flytesnacks-core.tar.gz  ./core/_pb_output

allPluginSnacks=("hive","k8s-spark","pod")
for plugin in ${allSnacks[@]}; do
  tar -zcvf ./release-snacks/flytesnacks-${plugin}.tar.gz  ./${plugin}/_pb_output
done