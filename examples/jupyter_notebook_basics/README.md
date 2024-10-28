(interactive-mode)=

# Jupyter Notebook Basic Development Guide

```{eval-rst}
.. tags:: Integration, Jupyter
```

```{image} https://img.shields.io/badge/Blog-Interactive-blue?style=for-the-badge
:target: https://hackmd.io/@1E0FEh2MS_OpXGUAjEFIOQ/ByTTT821Jl
:alt: Interactive Mode for Jupyter Notebook Blog Post
```

Jupyter Notebooks revolutionize workflow development by combining code execution, documentation, and visualization in one interactive environment. Through Flyte's integration, you can develop and test your workflows remotely while maintaining production-ready scalability—eliminating the gap between development and deployment.

## How to Use the Interactive Mode?

Interactive mode is a feature included in [FlyteRemote](https://docs.flyte.org/en/latest/api/flytekit/design/control_plane.html) aiming at supporting entities (tasks, workflows, launch plans, etc.) registration and execution within interactive environment like Jupyter Notebook. To use the interactive mode, you just need to create a FlyteRemote object with `interactive_mode_enabled=True` to interact with Flyte backend. Then you are free to go!

For detailed examples and usage patterns, refer to the following guide:

```{auto-examples-toc}
basic
```
