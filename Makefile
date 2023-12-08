export REPOSITORY=flytesnacks
include boilerplate/flyte/end2end/Makefile
.SILENT:

define PIP_COMPILE
pip-compile  $(1) ${PIP_ARGS} --upgrade --verbose --resolver=backtracking
endef

install-piptools:
	pip install pip-tools

dev-requirements.txt: export CUSTOM_COMPILE_COMMAND := $(MAKE) dev-requirements.txt
dev-requirements.txt: dev-requirements.in install-piptools
	$(call PIP_COMPILE,dev-requirements.in)

.PHONY: dev-requirements
dev-requirements: dev-requirements.txt

docs-requirements.txt: export CUSTOM_COMPILE_COMMAND := $(MAKE) docs-requirements.txt
docs-requirements.txt: docs-requirements.in install-piptools
	$(call PIP_COMPILE,docs-requirements.in)

.PHONY: docs-requirements
docs-requirements: docs-requirements.txt

.PHONY: fmt
fmt: ## Format code with black and isort
	autoflake --remove-all-unused-imports --ignore-init-module-imports --ignore-pass-after-docstring --in-place -r examples
	pre-commit run black --all-files || true
	pre-commit run isort --all-files || true

.PHONY: update_boilerplate
update_boilerplate:
	@boilerplate/update.sh
