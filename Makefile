export REPOSITORY=flytesnacks

.SILENT:

# Flyte sandbox configuration variables
KUBERNETES_API_PORT := 30086
FLYTE_PROXY_PORT := 30081
K8S_DASHBOARD_PROXY_PORT := 30082
MINIO_PROXY_PORT := 30084
FLYTE_SANDBOX_NAME := flyte-sandbox
FLYTE_DIR := ~/.flyte

# Module of cookbook examples to register
EXAMPLES_MODULE := core

define LOG
echo "$(shell tput bold)$(shell tput setaf 2)$(1)$(shell tput sgr0)"
endef

.PHONY: update_boilerplate
update_boilerplate:
	@curl https://raw.githubusercontent.com/flyteorg/boilerplate/master/boilerplate/update.sh -o boilerplate/update.sh
	@boilerplate/update.sh


.PHONY: help
help: ## Show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# Helper to determine if a sandbox is up and running
.PHONY: _requires-sandbox-up
_requires-sandbox-up:
ifeq ($(shell docker ps -f name=$(FLYTE_SANDBOX_NAME) --format={.ID}),)
	$(error Cluster has not been started! Use 'make start' to start a cluster)
endif

.PHONY: setup
setup:
	$(call LOG,Starting Flyte sandbox)
	flytectl sandbox start --source=$(shell pwd)

.PHONY: start
start: setup setup-config

	$(call LOG,Registering examples from commit: latest)

	REGISTRY=cr.flyte.org/flyteorg VERSION=latest make -C cookbook/$(EXAMPLES_MODULE) fast_register

.PHONY: teardown
teardown: _requires-sandbox-up  ## Teardown Flyte sandbox
	$(call LOG,Tearing down Flyte sandbox)
	flytectl sandbox teardown

.PHONY: status
status: _requires-sandbox-up  ## Show status of Flyte deployment
	kubectl get pods -n flyte

.PHONY: shell
shell: _requires-sandbox-up  ## Drop into a development shell
	docker exec -it flyte-sandbox bash

.PHONY: register
register: _requires-sandbox-up  ## Register Flyte cookbook workflows
	$(call LOG,Registering example workflows in cookbook/$(EXAMPLES_MODULE))
	make -C cookbook/$(EXAMPLES_MODULE) register

.PHONY: fast_register
fast_register: _requires-sandbox-up  ## Fast register Flyte cookbook workflows
	$(call LOG,Fast registering example workflows in cookbook/$(EXAMPLES_MODULE))
	make -C cookbook/$(EXAMPLES_MODULE) fast_register

.PHONY: setup-kubectl
kubectl-config:
	echo "export KUBECONFIG=$(KUBECONFIG):~/.kube/config:$(FLYTE_DIR)/k3s/k3s.yaml"

.PHONY: setup-flytectl
setup-config: kubectl-config
	flytectl config init
