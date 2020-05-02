PROJECT=flytecookbook
DOMAIN=development
# Uncomment after adding the NOPUSH option to the build script
# REGISTRY=docker.io/lyft

.PHONY: docker_build
docker_build:
	flytekit_build_image.sh .

.PHONY: docker_build
docker_push:
	REGISTRY=docker.io/lyft flytekit_build_image.sh .

.PHONY: in_container_register_sandbox
in_container_register_sandbox:
	pyflyte -p ${PROJECT} -d ${DOMAIN} --config /root/sandbox.config register workflows
