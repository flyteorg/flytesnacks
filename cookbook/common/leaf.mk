.SILENT:

# This is used by the image building script referenced below. Normally it just takes the directory name but in this
# case we want it to be called something else.
IMAGE_NAME=flytecookbook
export VERSION ?= $(shell git rev-parse HEAD)

define PIP_COMPILE
pip-compile $(1) ${PIP_ARGS} --upgrade --verbose
endef

# Set SANDBOX=1 to automatically fill in sandbox config
ifdef SANDBOX

# The url for Flyte Control plane
export FLYTE_HOST ?= localhost:30081

# Overrides s3 url. This is solely needed for SANDBOX deployments. Shouldn't be overriden in production AWS S3.
export FLYTE_AWS_ENDPOINT ?= http://localhost:30084/

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

# setup output directory
ifndef OUTPUT_DIR
	export OUTPUT_DIR=${CURDIR}/
endif
# The docker registry that should be used to push images.
# e.g.:
# export REGISTRY ?= ghcr.io/flyteorg
endif

# The Flyte project that we want to register under
export PROJECT ?= flytesnacks

PATH_TO_EXAMPLE = $(shell echo "${CURDIR}" | grep -o "cookbook.*")

# If the REGISTRY environment variable has been set, that means the image name will not just be tagged as
#   flytecookbook:<sha> but rather,
#   ghcr.io/flyteorg/flytecookbook:<sha> or whatever your REGISTRY is.
ifdef REGISTRY
	FULL_IMAGE_NAME = ${REGISTRY}/${IMAGE_NAME}
	EXAMPLE_OUTPUT_DIR = ${CURDIR}/_pb_output
	COMMAND = docker
	BUILD_CONTEXT = ${CURDIR}/..
	DOCKER_FILE = Dockerfile
endif
ifndef REGISTRY
	FULL_IMAGE_NAME = ${IMAGE_NAME}
	EXAMPLE_OUTPUT_DIR = /root/${PATH_TO_EXAMPLE}/_pb_output
	COMMAND = flytectl sandbox exec -- docker
	BUILD_CONTEXT = /root/${PATH_TO_EXAMPLE}/..
	DOCKER_FILE = /root/${PATH_TO_EXAMPLE}/Dockerfile
endif

# If you are using a different service account on your k8s cluster, add SERVICE_ACCOUNT=my_account before your make command
ifndef SERVICE_ACCOUNT
	SERVICE_ACCOUNT=default
endif

requirements.txt: export CUSTOM_COMPILE_COMMAND := $(MAKE) requirements.txt
requirements.txt: requirements.in install-piptools
	$(call PIP_COMPILE,requirements.in)

.PHONY: requirements
requirements: requirements.txt

.PHONY: install_requirements
install_requirements: requirements
	@echo ${CURDIR}
	pip install -r requirements.txt


.PHONY: serialize
serialize: install_requirements docker_build
	@echo ${VERSION}
	pyflyte --pkgs ${PREFIX}  package --image ${TAGGED_IMAGE} --source=${CURDIR}/..  --force --output="${OUTPUT_DIR}flytesnacks_${PREFIX}.tgz"

.PHONY: fast_serialize
fast_serialize:
	@echo pyflyte --pkgs ${PREFIX} package --image ${TAGGED_IMAGE} --source=${CURDIR}/..  --force --fast --output="${OUTPUT_DIR}flytesnacks_${PREFIX}.tgz"

.PHONY: docker_build
docker_build:
	@eval ${COMMAND} build ${BUILD_CONTEXT} --build-arg tag="${TAGGED_IMAGE}" -t "${TAGGED_IMAGE}" -f ${DOCKER_FILE}

.PHONY: register
register: serialize docker_push
	@echo ${VERSION}
	@echo ${CURDIR}
	flytectl register files \
	    -p ${PROJECT} -d development \
	     --version=${VERSION} \
	     --k8ServiceAccount=$(SERVICE_ACCOUNT) \
	     --outputLocationPrefix=${OUTPUT_DATA_PREFIX} \
	     "${OUTPUT_DIR}flytesnacks_${PREFIX}.tgz" \
	     --archive

.PHONY: fast_register
fast_register: fast_serialize
	@echo ${VERSION}
	@echo ${CURDIR}
	flytectl register files \
	    -p ${PROJECT} -d development \
	     --version=${VERSION} \
	     --k8ServiceAccount=$(SERVICE_ACCOUNT) \
	     --outputLocationPrefix=${OUTPUT_DATA_PREFIX} \
	     "${OUTPUT_DIR}flytesnacks_${PREFIX}.tgz" \
	     --archive