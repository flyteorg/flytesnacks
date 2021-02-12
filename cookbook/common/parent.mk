# This is a Makefile you can include in directories that have child directories you want to build common flyte targets on.
SUBDIRS = $(shell ls -d */)
PWD=$(CURDIR)

.PHONY: all_fast_serialize
all_fast_serialize:
	for dir in $(SUBDIRS) ; do \
		trimmed=$${dir%/}; \
		PREFIX=$$trimmed make fast_serialize; \
	done

.PHONY: all_register
all_register:
	for dir in $(SUBDIRS) ; do \
		make -C  $$dir register; \
	done

.PHONY: all_serialize
all_serialize:
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir serialize; \
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
	echo "processing ${PWD}"
	for dir in $(SUBDIRS) ; do \
		echo "processing $$dir"; \
		make -C $$dir requirements; \
	done
