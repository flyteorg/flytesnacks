include cookbook/Makefile
.SILENT:

# Update PATH variable to leverage _bin directory
export PATH := .k3s/bin:$(PATH)

# Dependencies
export DOCKER_VERSION := 20.10.3
export K3S_VERSION := v1.20.2%2Bk3s1
export KUBECTL_VERSION := v1.20.2

# Flyte cluster configuration variables
DOCKER_BIND_PORT := 51234
KUBERNETES_API_PORT := 51235
FLYTE_PROXY_PORT := 51236
FLYTE_CLUSTER_NAME := k3s-flyte

# Use an ephemeral kubeconfig, so as not to litter the default one
export KUBECONFIG=$(PWD)/.k3s/data/config/kubeconfig

.PHONY: help
help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# Helper to determine if a cluster is up and running
.PHONY: _requires-active-cluster
_requires-active-cluster:
ifeq ($(shell docker ps -f name=$(FLYTE_CLUSTER_NAME) --format={.ID}),)
	$(error Cluster has not been started! Use 'make start' to start a cluster)
endif

.PHONY: _prepare
_prepare:
	.k3s/prepare.sh

.PHONY: start
start: _prepare  ## Start a local Flyte cluster
	docker run -d --rm --privileged --name $(FLYTE_CLUSTER_NAME) -e K3S_KUBECONFIG_OUTPUT=/config/kubeconfig -v /var/run -v $(PWD)/.k3s/data/config:/config -p $(KUBERNETES_API_PORT):$(KUBERNETES_API_PORT) -p $(FLYTE_PROXY_PORT):30081 k3s-dind:latest --https-listen-port $(KUBERNETES_API_PORT) --no-deploy=traefik --no-deploy=servicelb --no-deploy=local-storage --no-deploy=metrics-server > /dev/null
	timeout 600 sh -c "until kubectl cluster-info &> /dev/null; do sleep 1; done"
	# TODO switch to https://raw.githubusercontent.com/flyteorg/flyte/master/deployment/sandbox/flyte_generated.yaml
	kubectl apply -f https://raw.githubusercontent.com/flyteorg/flyte/07734da0a902887678a7901114dbd96481aeecbc/deployment/sandbox/flyte_generated.yaml
	kubectl wait --for=condition=available deployment/{datacatalog,flyteadmin,flyteconsole,flytepropeller} -n flyte --timeout=10m

.PHONY: teardown
teardown: _requires-active-cluster  ## Teardown Flyte cluster
	docker rm -f -v $(FLYTE_CLUSTER_NAME)

.PHONY: status
status: _requires-active-cluster  ## Show status of Flyte deployment
	kubectl get pods -n flyte

.PHONY: console
console: _requires-active-cluster  ## Open Flyte console
	open "http://localhost:$(FLYTE_PROXY_PORT)/console"

.PHONY: _build-task-image
_build-task-image: _requires-active-cluster
	docker run -it --rm --volumes-from $(FLYTE_CLUSTER_NAME) -e DOCKER_BUILDKIT=1 -v $(PWD)/cookbook:/workspace --entrypoint="" k3s-dind:latest docker build -f /workspace/core/Dockerfile -t cookbook /workspace
