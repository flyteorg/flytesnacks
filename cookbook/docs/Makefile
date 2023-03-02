.PHONY: rsts
rsts:
	sphinx-apidoc --force --tocfile index --ext-autodoc --output-dir _rsts ../../

.PHONY: html
html:
	sphinx-build ${SPHINXOPTS} -W -n -b html . _build

.PHONY: linkcheck
linkcheck:
	sphinx-build -n -b linkcheck . _build

.PHONY: doctest
doctest:
	sphinx-build -n -b doctest . _build

.PHONY: clear-cache
clear-cache:
	pyflyte local-cache clear

.PHONY: clean
clean: clear-cache
	rm -rf _build
	rm -rf auto_*
	rm -rf auto/*
	rm -rf _tags/*
