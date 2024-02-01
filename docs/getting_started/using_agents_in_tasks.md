---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
---

# Using Flyte agents in tasks

If you need to connect to an external service in your workflow, we recommend using the corresponding agent rather than a web API plugin. Unlike web API plugins, agents do not require creating a Kubernetes pod for each task. Agents are designed to be scalable and can handle large workloads efficiently, and decrease load on FlytePropeller, since they run outside of it. Finally, you can test agents locally without having to change the Flyte backend configuration, streamlining development.

TK - example
