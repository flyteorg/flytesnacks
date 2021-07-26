.SILENT:

include common/Makefile
include common/parent.mk

define PIP_COMPILE
pip-compile $(1) ${PIP_ARGS} --upgrade --verbose
endef

dev-requirements.txt: export CUSTOM_COMPILE_COMMAND := $(MAKE) dev-requirements.txt
dev-requirements.txt: dev-requirements.in install-piptools
	$(call PIP_COMPILE,dev-requirements.in)

dev-requirements: dev-requirements.txt
	pip install -r dev-requirements.txt

docs-requirements.txt: export CUSTOM_COMPILE_COMMAND := $(MAKE) docs-requirements.txt
docs-requirements.txt: docs-requirements.in install-piptools
	$(call PIP_COMPILE,docs-requirements.in)

.PHONY: docs-requirements
docs-requirements: docs-requirements.txt

.PHONE: run-all-examples
run-examples: ## Runs all examples
	sh scripts/run-all-examples.sh


