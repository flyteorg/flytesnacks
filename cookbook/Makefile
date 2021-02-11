include common/Makefile

PWD=$(CURDIR)

.PHONY: enter_sandbox
enter_sandbox: docker_build
	docker run -e PROJECT=${PROJECT} -v `pwd`:/root -it ${FULL_IMAGE_NAME}:${VERSION} bash

.PHONE: run-all-examples
run-examples:
	sh ./scripts/run-all-examples.sh

.PHONY: all_fast_serialize
all_fast_serialize:
	make -C core fast_serialize
	make -C plugins all_fast_serialize
	make -C case_studies all_fast_serialize

.PHONY: all_docker_push
all_docker_push: docker_push
	$(MAKE) -C plugins all_docker_push

.PHONY: all_requirements
all_requirements: requirements
	ENV_BASE_PATH="${PWD}/env/" scripts/make-all-docker.sh requirements

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
