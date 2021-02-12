# This is used by the image building script referenced below. Normally it just takes the directory name but in this
# case we want it to be called something else.
IMAGE_NAME=flytecookbook
VERSION=$(shell git rev-parse HEAD)

define PIP_COMPILE
pip-compile $(1) ${PIP_ARGS} --upgrade --verbose
endef

# If the REGISTRY environment variable has been set, that means the image name will not just be tagged as
#   flytecookbook:<sha> but rather,
#   ghcr.io/flyteorg/flytecookbook:<sha> or whatever your REGISTRY is.
ifneq ($(origin REGISTRY), undefined)
	FULL_IMAGE_NAME = ${REGISTRY}/${IMAGE_NAME}
else
	FULL_IMAGE_NAME = ${IMAGE_NAME}
endif

# If you're port-forwarding your service or running the sandbox Flyte deployment, just don't specify anything.
# If your Flyte Admin is behind SSL, add SECURE=1 before your make command
ifneq ($(origin SECURE), undefined)
	INSECURE_FLAG =
else
	INSECURE_FLAG = -i
endif

# If you are using a different service account on your k8s cluster, add SERVICE_ACCOUNT=my_account before your make command
ifndef SERVICE_ACCOUNT
	SERVICE_ACCOUNT=default
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

TAGGED_IMAGE=${FULL_IMAGE_NAME}:${PREFIX}-${VERSION}

# This should only be used by Admins to push images to the public Dockerhub repo. Make sure you
# specify REGISTRY=ghcr.io/flyteorg or your registry before the make command otherwise this won't actually push
# Also if you want to push the docker image for sagemaker consumption then
# specify ECR_REGISTRY
.PHONY: docker_push
docker_push: docker_build
	docker push ${TAGGED_IMAGE}

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

requirements.txt: export CUSTOM_COMPILE_COMMAND := make requirements.txt
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
	flyte-cli fast-register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p flytetester -d development --kubernetes-service-account ${SERVICE_ACCOUNT} --output-location-prefix ${OUTPUT_DATA_PREFIX} --additional-distribution-dir ${ADDL_DISTRIBUTION_DIR} _pb_output/*

.PHONY: fast_register_sandbox
fast_register_sandbox: fast_serialize_sandbox
	echo "Registering against localhost. Follow the README to use a remote Flyte installation"
	FLYTE_AWS_ENDPOINT=http://localhost:9000/ FLYTE_AWS_ACCESS_KEY_ID=minio FLYTE_AWS_SECRET_ACCESS_KEY=miniostorage \
		flyte-cli fast-register-files -h localhost:80 ${INSECURE_FLAG} -p ${PROJECT} -d development ${INSECURE_FLAG} \
		--additional-distribution-dir s3://my-s3-bucket/fast/ --dest-dir /root/recipes ${CURDIR}/_pb_output/*

.PHONY: fast_serialize_sandbox
fast_serialize_sandbox:
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm -f ${CURDIR}/_pb_output/*.tar.gz
	docker run -v ${CURDIR}/_pb_output:/tmp/output -v  ${TAGGED_IMAGE} make fast_serialize_sandbox

.PHONY: docker_build
docker_build:
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
	docker run -v ${CURDIR}/_pb_output:/tmp/output ${TAGGED_IMAGE} make serialize
