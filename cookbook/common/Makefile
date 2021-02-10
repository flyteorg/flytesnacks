# This is used by the image building script referenced below. Normally it just takes the directory name but in this
# case we want it to be called something else.
IMAGE_NAME=flytecookbook
# VERSION=$(shell echo git rev-parse HEAD)
# PREV_BUILD_HASH = $(shell cat build-hash || echo “”)
VERSION=$(shell git rev-parse HEAD)

define PIP_COMPILE
pip-compile $(1) --upgrade --verbose
endef

# If the REGISTRY environment variable has been set, that means the image name will not just be tagged as
#   flytecookbook:<sha> but rather,
#   ghcr.io/flyteorg/flytecookbook:<sha> or whatever your REGISTRY is.
ifneq ($(origin REGISTRY), undefined)
	FULL_IMAGE_NAME = ${REGISTRY}/${IMAGE_NAME}
else
	FULL_IMAGE_NAME = ${IMAGE_NAME}
endif

# The Flyte project that we want to register under
PROJECT=flytesnacks

.SILENT: help
.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: debug
debug:
	echo "IMAGE NAME ${IMAGE_NAME}"
	echo "FULL IMAGE NAME ${FULL_IMAGE_NAME}"
	echo "VERSION TAG ${VERSION}"
	echo "REGISTRY ${REGISTRY}"

# This should only be used by Admins to push images to the public Dockerhub repo. Make sure you
# specify REGISTRY=ghcr.io/flyteorg or your registry before the make command otherwise this won't actually push
# Also if you want to push the docker image for sagemaker consumption then
# specify ECR_REGISTRY
.PHONY: docker_push
docker_push:
	DOCKER_BUILDKIT=1 IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh ../${PREFIX}.Dockerfile ${PREFIX}

.PHONY: fmt
fmt: ## Format code with black and isort
	black .
	isort .

.PHONY: install-piptools
install-piptools:
	pip install -U pip-tools

.PHONY: setup
setup: install-piptools ## Install requirements
	pip-sync dev-requirements.txt

.PHONY: lint
lint: ## Run linters
	flake8 .

dev-requirements.txt: export CUSTOM_COMPILE_COMMAND := make dev-requirements.txt
dev-requirements.txt: dev-requirements.in install-piptools
	$(call PIP_COMPILE,dev-requirements.in)

requirements.txt: export CUSTOM_COMPILE_COMMAND := make requirements.txt
requirements.txt: requirements.in install-piptools
	$(call PIP_COMPILE,requirements.in)

.PHONY: requirements
requirements: requirements.txt dev-requirements.txt

.PHONY: in_container_serialize_sandbox
in_container_serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/output

.PHONY: docker_build
docker_build:
	DOCKER_BUILDKIT=1 NOPUSH=1 IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh ../${PREFIX}.Dockerfile ${PREFIX}

.PHONY: register_sandbox
register_sandbox: docker_build serialize_sandbox
	test $(FLYTE_HOST) || ( echo ">> FLYTE_HOST is not set"; exit 1 )
	flyte-cli register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p ${PROJECT} -d development -v ${VERSION} ${CURDIR}/_pb_output/*

.PHONY: serialize_sandbox
serialize_sandbox: docker_build
	echo ${VERSION}
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	docker run -v ${CURDIR}/_pb_output:/tmp/output ${FULL_IMAGE_NAME}:${PREFIX}-${VERSION} make in_container_serialize_sandbox
