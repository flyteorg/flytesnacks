#!/usr/bin/env bash
#
set -e


flytectl sandbox exec -- docker build . --tag "rawcontainers:$1"
pyflyte --pkgs flyte.workflows package --image "rawcontainers:$1" -f
flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz  --version "$1"
