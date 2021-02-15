.SILENT:

# This is used by the image building script referenced below. Normally it just takes the directory name but in this
# case we want it to be called something else.
IMAGE_NAME=flytecookbook
VERSION=$(shell git rev-parse HEAD)

define PIP_COMPILE
pip-compile $(1) ${PIP_ARGS} --upgrade --verbose
endef

# Set SANDBOX=1 to automatically fill in sandbox config
ifdef SANDBOX

# The url for Flyte Control plane
export FLYTE_HOST ?= localhost:8001

# Overrides s3 url. This is solely needed for SANDBOX deployments. Shouldn't be overriden in production AWS S3.
export FLYTE_AWS_ENDPOINT ?= http://localhost:9000/

# Used to authenticate to s3. For a production AWS S3, it's discouraged to use keys and key ids.
export FLYTE_AWS_ACCESS_KEY_ID ?= minio

# Used to authenticate to s3. For a production AWS S3, it's discouraged to use keys and key ids.
export FLYTE_AWS_SECRET_ACCESS_KEY ?= miniostorage

# Used to publish artifacts for fast registration
export ADDL_DISTRIBUTION_DIR ?= s3://my-s3-bucket/fast/

# The base of where Blobs, Schemas and other offloaded types are, by default, serialized.
export OUTPUT_DATA_PREFIX ?= s3://my-s3-bucket/raw-data

# Instructs flyte-cli commands to use insecure channel when communicating with Flyte's control plane.
# If you're port-forwarding your service or running the sandbox Flyte deployment, specify INSECURE=1 before your make command.
# If your Flyte Admin is behind SSL, don't specify anything.
ifndef INSECURE
	export INSECURE_FLAG=-i
endif

# The Flyte project that we want to register under
export PROJECT ?= flytesnacks

# The docker registry that should be used to push images.
# e.g.: 
# export REGISTRY ?= ghcr.io/flyteorg
endif

# If the REGISTRY environment variable has been set, that means the image name will not just be tagged as
#   flytecookbook:<sha> but rather,
#   ghcr.io/flyteorg/flytecookbook:<sha> or whatever your REGISTRY is.
ifdef REGISTRY
	FULL_IMAGE_NAME = ${REGISTRY}/${IMAGE_NAME}
endif
ifndef REGISTRY
	FULL_IMAGE_NAME = ${IMAGE_NAME}
endif

# If you are using a different service account on your k8s cluster, add SERVICE_ACCOUNT=my_account before your make command
ifndef SERVICE_ACCOUNT
	SERVICE_ACCOUNT=default
endif

.PHONY: help
help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: debug
debug:
	echo "IMAGE NAME ${IMAGE_NAME}"
	echo "FULL IMAGE NAME ${FULL_IMAGE_NAME}"
	echo "VERSION TAG ${VERSION}"
	echo "REGISTRY ${REGISTRY}"

TAGGED_IMAGE=${FULL_IMAGE_NAME}:${PREFIX}-${VERSION}

# This should only be used by Admins to push images to the public Dockerhub repo. Make sure you
# specify REGISTRY=ghcr.io/flyteorg or your registry before the make command otherwise this won't actually push
# Also if you want to push the docker image for sagemaker consumption then
# specify ECR_REGISTRY
.PHONY: docker_push
docker_push: docker_build
ifdef REGISTRY
	docker push ${TAGGED_IMAGE}
endif

.PHONY: fmt
fmt: # Format code with black and isort
	black .
	isort .

.PHONY: install-piptools
install-piptools:
	pip install -U pip-tools

.PHONY: setup
setup: install-piptools # Install requirements
	pip-sync dev-requirements.txt

.PHONY: lint
lint:  # Run linters
	flake8 .

requirements.txt: export CUSTOM_COMPILE_COMMAND := $(MAKE) requirements.txt
requirements.txt: requirements.in install-piptools
	$(call PIP_COMPILE,requirements.in)

.PHONY: requirements
requirements: requirements.txt

.PHONY: fast_serialize
fast_serialize:
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	pyflyte -c sandbox.config --pkgs ${PREFIX} serialize --in-container-config-path /root/sandbox.config --local-source-root ${CURDIR} --image ${FULL_IMAGE_NAME}:${PREFIX}-${VERSION} fast workflows -f _pb_output/

.PHONY: fast_register
fast_register:
	test $(OUTPUT_DATA_PREFIX) || ( echo ">> OUTPUT_DATA_PREFIX is not set"; exit 1 )
	test $(FLYTE_HOST) || ( echo ">> FLYTE_HOST is not set"; exit 1 )
	test $(ADDL_DISTRIBUTION_DIR) || ( echo ">> ADDL_DISTRIBUTION_DIR is not set"; exit 1 )
	flyte-cli fast-register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p ${PROJECT} -d development --kubernetes-service-account ${SERVICE_ACCOUNT} --output-location-prefix ${OUTPUT_DATA_PREFIX} \
		--additional-distribution-dir ${ADDL_DISTRIBUTION_DIR} _pb_output/*

.PHONY: fast_serialize
fast_serialize:
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm -f ${CURDIR}/_pb_output/*.tar.gz
	docker run -v ${CURDIR}/_pb_output:/tmp/output -v ${CURDIR}:/root/$(firstword $(subst /, ,$(CURDIR))) ${TAGGED_IMAGE} $(MAKE) fast_serialize

.PHONY: docker_build
docker_build:
	echo "Tagged Image: "
	echo ${TAGGED_IMAGE}
	docker build ../ --build-arg tag="${TAGGED_IMAGE}" -t "${TAGGED_IMAGE}" -f Dockerfile

.PHONY: register
register: docker_push serialize
	test $(FLYTE_HOST) || ( echo ">> FLYTE_HOST is not set"; exit 1 )
	flyte-cli register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p ${PROJECT} -d development -v ${VERSION} ${CURDIR}/_pb_output/*

.PHONY: serialize
serialize: docker_build
	@echo ${VERSION}
	@echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	docker run -v ${CURDIR}/_pb_output:/tmp/output ${TAGGED_IMAGE} $(MAKE) serialize

# Cluster Name used for k3d installation
export FLYTE_CLUSTER_NAME ?= flyte

.PHONY: k3d_load_image
k3d_load_image: docker_build
	k3d --cluster ${FLYTE_CLUSTER_NAME} image import ${TAGGED_IMAGE}

.PHONY: clean
clean:
	rm -rf _pb_output/