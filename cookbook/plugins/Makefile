include ../common/Makefile.common

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

.PHONY: register_sandbox
register_sandbox:
	../scripts/make_all_subdirs.sh register_sandbox

.PHONY: serialize_sandbox
serialize_sandbox:
	../scripts/make_all_subdirs.sh serialize_sandbox

PWD=$(CURDIR)
.PHONY: docker_push
docker_push:
	../scripts/make_all_subdirs.sh docker_push

.PHONY: requirements
requirements: requirements
	ENV_BASE_PATH="${PWD}/env/" ../scripts/make-all-docker.sh requirements
