PROJECT=flytecookbook
DOMAIN=development

.PHONY: docker_build
docker_build:
	flytekit_build_image.sh .

.PHONY: docker_build
docker_push:
	REGISTRY=docker.io/lyft/flytecookbook flytekit_build_image.sh .
