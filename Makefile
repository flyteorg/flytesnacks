.SILENT:

# Dependencies
export K3D_VERSION := v4.2.0
export KUBECTL_VERSION := v1.20.2

# Flyte cluster configuration variables
FLYTE_CLUSTER_NAME := flyte
FLYTE_CLUSTER_CONTEXT := k3d-$(FLYTE_CLUSTER_NAME)
FLYTE_PROXY_PORT := 8001

# Use an ephemeral kubeconfig, so as not to litter the default one
export KUBECONFIG=$(HOME)/.k3d/kubeconfig-$(FLYTE_CLUSTER_NAME).yaml

.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: _install-demo-deps
_install-demo-deps:
	scripts/install_demo_deps.sh

.PHONY: start
start: _install-demo-deps  ## Start a local Flyte cluster
	_bin/k3d cluster create -p "$(FLYTE_PROXY_PORT):30081" --no-lb --k3s-server-arg '--no-deploy=traefik' --k3s-server-arg '--no-deploy=servicelb' --kubeconfig-update-default $(FLYTE_CLUSTER_NAME)
	_bin/k3d kubeconfig write $(FLYTE_CLUSTER_NAME)
	_bin/kubectl --context $(FLYTE_CLUSTER_CONTEXT) apply -f https://raw.githubusercontent.com/flyteorg/flyte/master/deployment/sandbox/flyte_generated.yaml
	_bin/kubectl --context $(FLYTE_CLUSTER_CONTEXT) wait --for=condition=available deployment/{datacatalog,flyteadmin,flyteconsole,flytepropeller} -n flyte --timeout=10m

.PHONY: teardown
teardown: _install-demo-deps  ## Teardown the local Flyte cluster
	_bin/k3d cluster delete $(FLYTE_CLUSTER_NAME)

.PHONY: status
status: _install-demo-deps  ## Show status of Flyte deployment
	kubectl --context $(FLYTE_CLUSTER_CONTEXT) get pods -n flyte

.PHONY: console
console: _install-demo-deps  ## Open Flyte console
	open "http://localhost:$(FLYTE_PROXY_PORT)/console"
