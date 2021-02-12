.SILENT:

# Update PATH variable to leverage _bin directory
export PATH := _bin:$(PATH)

# Dependencies
export K3D_VERSION := v4.2.0
export KUBECTL_VERSION := v1.20.2

# Flyte cluster configuration variables
FLYTE_CLUSTER_NAME := flyte
FLYTE_CLUSTER_CONTEXT := k3d-$(FLYTE_CLUSTER_NAME)
FLYTE_PROXY_PORT := 8001

# Use an ephemeral kubeconfig, so as not to litter the default one
export KUBECONFIG=$(HOME)/.k3d/kubeconfig-$(FLYTE_CLUSTER_NAME).yaml

# Helper to determine if a cluster is up and running - uses the ephemeral kubeconfig
# as a flag
IS_UP = $(shell [ -f $(KUBECONFIG) ] && echo true)

.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: _requires-active-cluster
_requires-active-cluster:
	ifneq ($(IS_UP),true)
		$(error Cluster has not been started! Use 'make start' to start a cluster)
	endif

.PHONY: _install-cluster-deps
_install-cluster-deps:
	scripts/install_cluster_deps.sh

.PHONY: start
start: _install-cluster-deps  ## Start a local Flyte cluster
	k3d cluster create -p "$(FLYTE_PROXY_PORT):30081" --no-lb --k3s-server-arg '--no-deploy=traefik' --k3s-server-arg '--no-deploy=servicelb' --kubeconfig-update-default=false $(FLYTE_CLUSTER_NAME)
	kubectl --context $(FLYTE_CLUSTER_CONTEXT) apply -f https://raw.githubusercontent.com/flyteorg/flyte/master/deployment/sandbox/flyte_generated.yaml
	kubectl --context $(FLYTE_CLUSTER_CONTEXT) wait --for=condition=available deployment/{datacatalog,flyteadmin,flyteconsole,flytepropeller} -n flyte --timeout=10m
	k3d kubeconfig write $(FLYTE_CLUSTER_NAME)

.PHONY: teardown
teardown: _requires-active-cluster _install-cluster-deps  ## Teardown the local Flyte cluster
	k3d cluster delete $(FLYTE_CLUSTER_NAME)

.PHONY: status
status: _requires-active-cluster _install-cluster-deps  ## Show status of Flyte deployment
	kubectl --context $(FLYTE_CLUSTER_CONTEXT) get pods -n flyte

.PHONY: console
console: _requires-active-cluster _install-cluster-deps  ## Open Flyte console
	open "http://localhost:$(FLYTE_PROXY_PORT)/console"
