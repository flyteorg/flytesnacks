# This is used by the image building script referenced below. Normally it just takes the directory name but in this
# case we want it to be called something else.
IMAGE_NAME=flytecookbook
VERSION=$(shell ./version.sh)

# The Flyte project that we want to register under
PROJECT=flytesnacks
DOMAIN=development
REGISTRY=docker.io/lyft

.PHONY: docker_build
docker_build:
	NOPUSH=1 REGISTRY=${REGISTRY} IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh .

.PHONY: docker_build
docker_push:
	IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} flytekit_build_image.sh .

.PHONY: in_container_register_sandbox
in_container_register_sandbox:
	pyflyte -p ${PROJECT} -d development --config /root/sandbox.config register workflows

.PHONY: register_sandbox
register_sandbox: docker_push
	docker run docker.io/lyft/flytecookbook:${VERSION} /usr/local/bin/flytekit_venv make in_container_register_sandbox

.PHONY: register_staging_in_container
register_staging_in_container:
	pyflyte -p ${PROJECT} -d ${DOMAIN} --config /root/staging.config register workflows

.PHONY: register_staging
register_staging: docker_push
	docker run -e FLYTE_CREDENTIALS_CLIENT_ID=${FLYTE_CREDENTIALS_CLIENT_ID} \
	-e FLYTE_CREDENTIALS_CLIENT_SECRET=${FLYTE_CREDENTIALS_CLIENT_SECRET} \
	-e FLYTE_CREDENTIALS_AUTH_MODE=basic -e FLYTE_CREDENTIALS_AUTHORIZATION_METADATA_KEY=flyte-authorization \
	-e FLYTE_CREDENTIALS_SCOPE=svc -e FLYTE_PLATFORM_AUTH=True \
	docker.io/lyft/${IMAGE_NAME}:${VERSION} /usr/local/bin/flytekit_venv make register_staging_in_container

.PHONY: register_production_in_container
register_production_in_container:
	pyflyte -p ${PROJECT} -d ${DOMAIN} --config /root/production.config register workflows

.PHONY: register_production
register_production: docker_push
	docker run -e FLYTE_CREDENTIALS_CLIENT_ID=${FLYTE_CREDENTIALS_CLIENT_ID} \
	-e FLYTE_CREDENTIALS_CLIENT_SECRET=${FLYTE_CREDENTIALS_CLIENT_SECRET} \
	-e FLYTE_CREDENTIALS_AUTH_MODE=basic -e FLYTE_CREDENTIALS_AUTHORIZATION_METADATA_KEY=flyte-authorization \
	-e FLYTE_CREDENTIALS_SCOPE=svc -e FLYTE_PLATFORM_AUTH=True \
	docker.io/lyft/${IMAGE_NAME}:${VERSION} /usr/local/bin/flytekit_venv make register_production_in_container

.PHONY: in_container_serialize_sandbox
in_container_serialize_sandbox:
	pyflyte -p ${PROJECT} -d development --config /root/sandbox.config serialize workflows -f /tmp/output

# TODO: Get rid of the backticks in the future
.PHONY: serialize_sandbox
serialize_sandbox: docker_push
	mkdir `pwd`/_pb_output || true
	docker run -v `pwd`/_pb_output:/tmp/output docker.io/lyft/flytecookbook:${VERSION} make in_container_serialize_sandbox

.PHONY: enter_sandbox
enter_sandbox: docker_build
	docker run -e PROJECT=${PROJECT} -v `pwd`:/root -it docker.io/lyft/flytecookbook:${VERSION} bash

.PHONY: book
book:
	@docker run -t -v `pwd`:/base lyft/docbuilder:v2.2.0 sphinx-build -E -b html /base/ /base/_build
