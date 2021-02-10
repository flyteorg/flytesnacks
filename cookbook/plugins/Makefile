include ../common/Makefile

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

SUBDIRS = $(shell ls -d */)
PWD=$(CURDIR)

.PHONY: register_sandbox
register_sandbox:
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

.PHONY: docker_push
docker_push:
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir docker_push; \
	done

.PHONY: requirements
requirements: requirements
	ENV_BASE_PATH="${PWD}/env/" ../scripts/make-all-docker.sh requirements
