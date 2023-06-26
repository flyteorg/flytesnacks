# Flyte Examples

This directory contains a series of example projects that demonstrate how to use
Flyte. The basic structure of the examples is as follows:

```{code-block} bash
example_project
├── README.md  # High-level description of the example project
├── Dockerfile  # Dockerfile for packaging up the project requirements
├── requirements.in  # Minimal python requirements for the project
├── requirements.txt  # Compiled python requirements using pip-compile
└── example_project  # Python package containing examples with the same name as the project
    ├── __init__.py
    ├── example_01.py
    ├── example_02.py
    ├── ...
    └── example_n.py
```

These example projects are meant to be stand-alone projects that can be built
and run by themselves.
