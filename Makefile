.SILENT:

# Update PATH variable to leverage _bin directory
export PATH := .sandbox/bin:$(PATH)

# Dependencies
export DOCKER_VERSION := 20.10.3
export K3S_VERSION := v1.20.2%2Bk3s1
export KUBECTL_VERSION := v1.20.2
export FLYTE_SANDBOX_IMAGE := flyte-sandbox:latest

# Flyte sandbox configuration variables
KUBERNETES_API_PORT := 51234
FLYTE_PROXY_PORT := 51235
FLYTE_SANDBOX_NAME := flyte-sandbox

# Use an ephemeral kubeconfig, so as not to litter the default one
export KUBECONFIG=$(PWD)/.sandbox/data/config/kubeconfig

define LOG
echo $(shell tput bold)$(shell tput setaf 2)$(1)$(shell tput sgr0)
endef

define RUN_IN_SANDBOX
docker run -it --rm \
	--network $(FLYTE_SANDBOX_NAME) \
	-e MAKEFLAGS \
	-e DOCKER_BUILDKIT=1 \
	--volumes-from $(FLYTE_SANDBOX_NAME) \
	-v $(PWD):/mnt/src \
	-w /usr/src \
	$(1) \
	$(FLYTE_SANDBOX_IMAGE) \
	with-src-snapshot.sh $(2)
endef

.PHONY: help
help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# Helper to determine if a sandbox is up and running
.PHONY: _requires-sandbox-up
_requires-sandbox-up:
ifeq ($(shell docker ps -f name=$(FLYTE_SANDBOX_NAME) --format={.ID}),)
	$(error Cluster has not been started! Use 'make start' to start a cluster)
endif

.PHONY: _prepare
_prepare:
	$(call LOG,Preparing dependencies)
	.sandbox/prepare.sh

.PHONY: start
start: _prepare  ## Start a local Flyte sandbox
	$(call LOG,Starting sandboxed Kubernetes cluster)
	docker network create $(FLYTE_SANDBOX_NAME) > /dev/null ||:
	docker run -d --rm --privileged --network $(FLYTE_SANDBOX_NAME) --name $(FLYTE_SANDBOX_NAME) -e KUBERNETES_API_PORT=$(KUBERNETES_API_PORT) -e K3S_KUBECONFIG_OUTPUT=/config/kubeconfig -v $(PWD)/.sandbox/data/config:/config -v /var/run -p $(KUBERNETES_API_PORT):$(KUBERNETES_API_PORT) -p $(FLYTE_PROXY_PORT):30081 $(FLYTE_SANDBOX_IMAGE) k3s-entrypoint.sh > /dev/null
	timeout 30 sh -c "until kubectl cluster-info &> /dev/null && sleep 1; do sleep 1; done"

	$(call LOG,Deploying Flyte)
	kubectl apply -f https://raw.githubusercontent.com/flyteorg/flyte/master/deployment/sandbox/flyte_generated.yaml
	kubectl wait --for=condition=available deployment/{datacatalog,flyteadmin,flyteconsole,flytepropeller} -n flyte --timeout=10m
	$(call LOG,"Flyte deployment ready! Flyte console is now available at http://localhost:$(FLYTE_PROXY_PORT)/console.")

.PHONY: teardown
teardown: _requires-sandbox-up  ## Teardown Flyte sandbox
	$(call LOG,Tearing down Flyte sandbox)
	docker rm -f -v $(FLYTE_SANDBOX_NAME) > /dev/null
	docker network rm $(FLYTE_SANDBOX_NAME) > /dev/null ||:

.PHONY: status
status: _requires-sandbox-up  ## Show status of Flyte deployment
	kubectl get pods -n flyte

.PHONY: register
register: _requires-sandbox-up  ## Register Flyte cookbook workflows
	$(call LOG,Registering example workflows)
	$(call RUN_IN_SANDBOX,-e SANDBOX=1 -e FLYTE_HOST=$(FLYTE_SANDBOX_NAME):30081,make -C cookbook/core register)
