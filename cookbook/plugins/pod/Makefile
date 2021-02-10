PREFIX=pod

include ../../common/Makefile.common

.PHONY: docker_push
docker_push:
	DOCKER_BUILDKIT=1 REGISTRY=${REGISTRY} IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh ../${PREFIX}.Dockerfile ${PREFIX}