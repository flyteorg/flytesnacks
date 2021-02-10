PREFIX=smpytorch
include ../../common/Makefile.common

.PHONY: in_container_serialize_sandbox
in_container_serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/output

.PHONY: register_sandbox
register_sandbox: docker_build serialize_sandbox
	test $(FLYTE_HOST) || ( echo ">> FLYTE_HOST is not set"; exit 1 )
	flyte-cli register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p ${PROJECT} -d development -v ${VERSION} ${CURDIR}/_pb_output/*

.PHONY: serialize_sandbox
serialize_sandbox: docker_build
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	docker run -v ${CURDIR}/_pb_output:/tmp/output ${FULL_IMAGE_NAME}:${PREFIX}-${VERSION} make in_container_serialize_sandbox

.PHONY: docker_build
docker_build:
	DOCKER_BUILDKIT=1 NOPUSH=1 IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh ./Dockerfile ${PREFIX}

.PHONY: docker_push
docker_push:
	DOCKER_BUILDKIT=1 IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh ../${PREFIX}.Dockerfile ${PREFIX}