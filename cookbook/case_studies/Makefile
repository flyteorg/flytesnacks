include ../common/Makefile

SUBDIRS = $(shell ls -d */)
PWD=$(CURDIR)

.PHONY: all_register_sandbox
all_register_sandbox:
	for dir in $(SUBDIRS) ; do \
		make -C  $$dir register_sandbox; \
	done

.PHONY: all_serialize_sandbox
all_serialize_sandbox:
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir serialize_sandbox; \
	done

.PHONY: all_docker_push
all_docker_push:
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir docker_push; \
	done

.PHONY: all_requirements
all_requirements:
	ENV_BASE_PATH="${PWD}/env/" ../scripts/make-all-docker.sh requirements
