#!/bin/bash

set -e

run() {
  Query=$(cat flytesnacks_manifest.json | jq -c '.[]| .path')
  if [ ! -z "$2" -a "$2" != " " ]; then
    Query=$(cat flytesnacks_manifest.json | jq -r --arg type $2 '.[]|select(.type | contains($type))| .path')
  fi
  for row in $Query; do
    echo "make -C cookbook/${row} $1"
  done
}

release() {
  Query=$(cat flytesnacks_manifest.json | jq -c '.[] | {path,id}')
  if [ ! -z "$1" -a "$1" != " " ]; then
    Query=$(cat flytesnacks_manifest.json | jq -c --arg type $1 '.[] | select(.type | contains($type)) | {path,id}')
  fi
  for row in $Query; do
    if [ -d "./cookbook/$(echo ${row} | jq -r '.path')/_pb_output/" ]; then
      tar -cvzf "./release-snacks/flytesnacks-$(echo ${row} | jq -r '.id').tgz"  "./cookbook/$(echo ${row} | jq -r '.path')/_pb_output/"
    fi
  done
}

if [ $1 == "release" ]; then
  mkdir -p release-snacks 
  release $2
else
  run $1 $2
fi 
