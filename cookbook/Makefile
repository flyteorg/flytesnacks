PROJECT=flytecookbook
DOMAIN=development
VERSION=$(shell ./version.sh)

.PHONY: docker_build
docker_build:
	flytekit_build_image.sh .

.PHONY: docker_build
docker_push:
	flytekit_build_image.sh .
