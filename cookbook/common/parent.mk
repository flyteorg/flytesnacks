# This is a Makefile you can include in directories that have child directories you want to build common flyte targets on.
SUBDIRS = $(shell ls -d */)
PWD=$(CURDIR)

.SILENT: help
.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: all_fast_serialize
all_fast_serialize:
	for dir in $(SUBDIRS) ; do \
		trimmed=$${dir%/}; \
		test -f $$dir/Dockerfile && \
		PREFIX=$$trimmed make fast_serialize; \
	done

.PHONY: all_fast_register
all_fast_register: ## Registers new code changes using the last built image (assumes current HEAD refers to a built image).
	for dir in $(SUBDIRS) ; do \
		trimmed=$${dir%/}; \
		test -f $$dir/Dockerfile && \
		PREFIX=$$trimmed make fast_register; \
	done

.PHONY: all_register
all_register: ## Builds, pushes and registers all docker images, workflows and tasks in all sub directories.
	for dir in $(SUBDIRS) ; do \
		make -C  $$dir register; \
	done

.PHONY: all_serialize
all_serialize: ## Builds and serializes all docker images, workflows and tasks in all sub directories.
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir serialize; \
	done

.PHONY: all_docker_push
all_docker_push: ## Builds and pushes all docker images.
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir docker_push; \
	done

.PHONY: all_requirements
all_requirements: ## Makes all requirement files in sub directories.
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir requirements; \
	done
