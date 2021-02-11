include common/Makefile

# If you're port-forwarding your service or running the sandbox Flyte deployment, just don't specify anything.
# If your Flyte Admin is behind SSL, add SECURE=1 before your make command
ifneq ($(origin SECURE), undefined)
	INSECURE_FLAG =
else
	INSECURE_FLAG = -i
endif

ifndef SERVICE_ACCOUNT
	SERVICE_ACCOUNT=default
endif

.PHONY: in_container_serialize_sandbox
in_container_serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/output

.PHONY: register_sandbox
register_sandbox: docker_build serialize_sandbox
	test $(FLYTE_HOST) || ( echo ">> FLYTE_HOST is not set"; exit 1 )
	flyte-cli register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p ${PROJECT} -d development -v ${VERSION} ${CURDIR}/_pb_output/*

.PHONY: serialize_sandbox
serialize_sandbox: dev_docker_build
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	docker run -v ${CURDIR}/_pb_output:/tmp/output ${FULL_IMAGE_NAME}:dev-${VERSION} make in_container_serialize_sandbox

.PHONY: serialize
serialize:
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	pyflyte -c sandbox.config --pkgs core serialize --in-container-config-path /root/sandbox.config --local-source-root ${CURDIR} --image ${FULL_IMAGE_NAME}:${VERSION} workflows -f _pb_output/

.PHONY: register
register:
	test $(OUTPUT_DATA_PREFIX) || ( echo ">> OUTPUT_DATA_PREFIX is not set"; exit 1 )
	test $(FLYTE_HOST) || ( echo ">> FLYTE_HOST is not set"; exit 1 )
	flyte-cli register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p flytetester -d development -v ${VERSION} --kubernetes-service-account ${SERVICE_ACCOUNT} --output-location-prefix ${OUTPUT_DATA_PREFIX} _pb_output/*

.PHONY: fast_serialize
fast_serialize:
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm ${CURDIR}/_pb_output/* || true
	pyflyte -c sandbox.config --pkgs core serialize --in-container-config-path /root/sandbox.config --local-source-root ${CURDIR} --image ${FULL_IMAGE_NAME}:${VERSION} fast workflows -f _pb_output/

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

.PHONY: in_container_fast_serialize_sandbox
in_container_fast_serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize fast workflows -f /tmp/output

.PHONY: fast_serialize_sandbox
fast_serialize_sandbox: dev_docker_build
	echo ${CURDIR}
	mkdir ${CURDIR}/_pb_output || true
	rm -f ${CURDIR}/_pb_output/*.tar.gz
	docker run -v ${CURDIR}/_pb_output:/tmp/output ${FULL_IMAGE_NAME}:dev-${VERSION} make in_container_fast_serialize_sandbox

.PHONY: enter_sandbox
enter_sandbox: docker_build
	docker run -e PROJECT=${PROJECT} -v `pwd`:/root -it ${FULL_IMAGE_NAME}:${VERSION} bash

.PHONE: run-all-examples
run-examples:
	sh ./scripts/run-all-examples.sh

PWD=$(CURDIR)
.PHONY: all_docker_push
all_docker_push: docker_push
	$(MAKE) -C plugins all_docker_push

.PHONY: all_requirements
all_requirements: requirements
	ENV_BASE_PATH="${PWD}/env/" scripts/make-all-docker.sh requirements

.PHONY: dev_docker_build
dev_docker_build:
	NOPUSH=1 IMAGE_NAME=${IMAGE_NAME} flytekit_build_image.sh ./dev.Dockerfile dev

.PHONY: all_register_sandbox
all_register_sandbox:
	make -C core register_sandbox
	make -C plugins all_register_sandbox
	make -C case_studies all_serialize_sandbox

.PHONY: all_serialize_sandbox
all_serialize_sandbox:
	make -C core serialize_sandbox
	make -C plugins all_serialize_sandbox
	make -C case_studies all_serialize_sandbox

.PHONY: all_docker_push
all_docker_push:
	make -C core docker_push
	make -C plugins all_docker_push
	make -C case_studies all_serialize_sandbox
