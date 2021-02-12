include common/Makefile

PWD=$(CURDIR)

dev-requirements.txt: export CUSTOM_COMPILE_COMMAND := make dev-requirements.txt
dev-requirements.txt: dev-requirements.in install-piptools
	$(call PIP_COMPILE,dev-requirements.in)

.PHONY: dev-requirements
dev-requirements: dev-requirements.txt

.PHONY: enter_sandbox
enter_sandbox: docker_build
	docker run -e PROJECT=${PROJECT} -v `pwd`:/root -it ${FULL_IMAGE_NAME}:${VERSION} bash

.PHONE: run-all-examples
run-examples: ## Runs all examples
	sh ./scripts/run-all-examples.sh

.PHONY: all_fast_register
all_fast_register: ## Registers new code changes using the last built image (assumes current HEAD refers to a built image).
	PREFIX=core make fast_register
	make -C plugins all_fast_register
	make -C case_studies all_fast_register

.PHONY: all_fast_serialize
all_fast_serialize:
	PREFIX=core make fast_serialize
	make -C plugins all_fast_serialize
	make -C case_studies all_fast_serialize

.PHONY: all_requirements
all_requirements: dev-requirements ## Makes all requirements in sub directories
	make -C core requirements
	make -C plugins all_requirements
	make -C case_studies all_requirements

.PHONY: all_register
all_register: ## Builds, pushes and registers all docker images, workflows and tasks in all sub directories.
	make -C core register
	make -C plugins all_register
	make -C case_studies all_register

.PHONY: all_serialize
all_serialize: ## Builds and serializes all docker images, workflows and tasks in all sub directories.
	make -C core serialize
	make -C plugins all_serialize
	make -C case_studies all_serialize

.PHONY: all_docker_push
all_docker_push: ## Builds and pushes all docker images.
	make -C core docker_push
	make -C plugins all_docker_push
	make -C case_studies all_docker_push

.PHONY: all_clean
all_clean: ## Cleans build directories
	PREFIX=core make clean
	make -C plugins all_clean
	make -C case_studies all_clean