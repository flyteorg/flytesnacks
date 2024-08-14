(ollama_plugin)=

# Ollama

```{eval-rst}
.. tags:: Inference, LLM
```

Serve large language models (LLMs) in a Flyte task.

[Ollama](https://ollama.com/) makes it easy to work with LLMs locally.
With the Ollama plugin, you can invoke model endpoints as if they were hosted on your machine, reducing network latency.

## Installation

To use the Ollama plugin, run the following command:

```
pip install flytekitplugins-inference
```

## Example usage

For a usage example, see {doc}`Ollama example usage <serve_llm>`.

```{note}
Ollama can only be run in a Flyte cluster, not locally, as it must be deployed as a sidecar service in a Kubernetes pod.
```

```{toctree}
:maxdepth: -1
:hidden:

serve_llm
```
