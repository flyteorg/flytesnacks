#!/bin/bash

set -e

run() {
  Query=$(cat flytesnacks_manifest.json | jq -r '.[]| .path')
  if [ ! -z "$2" -a "$2" != " " ]; then
    Query=$(cat flytesnacks_manifest.json | jq -r --arg type $2 '.[]|select(.type | contains($type))| .path')
  fi
  if [ ! -z "$3" -a "$3" != " " ]; then
    Query=$(cat flytesnacks_manifest.json | jq -r --arg type $2 --arg id $3 '.[]|select(.type | contains($type))| select(.id | contains($id)) | .path')
  fi
  for row in $Query; do
    make -C cookbook/${row} $1
  done
}

release() {
  Query=$(cat flytesnacks_manifest.json | jq -c '.[] | {path,id}')
  if [ ! -z "$1" -a "$1" != " " ]; then
    Query=$(cat flytesnacks_manifest.json | jq -c --arg type $1 '.[] | select(.type | contains($type)) | {path,id}')
  fi
  if [ ! -z "$2" -a "$2" != " " ]; then
    Query=$(cat flytesnacks_manifest.json | jq -c --arg type $1 --arg id $2 '.[] | select(.type | contains($type)) | select(.id | contains($id)) | {path,id}')
  fi
  for row in $Query; do
    if [[ -d "./cookbook/$(echo ${row} | jq -r '.path')/_pb_output/" ]]; then
      tar -cvzf "./release-snacks/flytesnacks-$(echo ${row} | jq -r '.id').tgz"  "./cookbook/$(echo ${row} | jq -r '.path')/_pb_output/"
    fi
  done
}


if [[ $1 == "release" ]]; then
  mkdir -p release-snacks 
  release $2 $3
else
  run $1 $2 $3
fi 
