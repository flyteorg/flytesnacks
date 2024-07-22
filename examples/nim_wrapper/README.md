(nim_wrapper)=

# NIM

```{eval-rst}
.. tags:: Inference, NVIDIA
```

Serve optimized model containers with NIM in a Flyte task.

[NVIDIA NIM](https://www.nvidia.com/en-in/ai/), part of NVIDIA AI Enterprise, provides a streamlined path
for developing AI-powered enterprise applications and deploying AI models in production.
It includes an out-of-the-box optimization suite, enabling AI model deployment across any cloud,
data center, or workstation. Since NIM can be self-hosted, there is greater control over cost, data privacy,
and more visibility into behind-the-scenes operations.

With NIM, you can invoke the model's endpoint as if it is hosted locally, minimizing network overhead.

NIM is available in Flytekit, and no additional packages are required to use the wrapper.

## Example usage

For a usage example, see {doc}`NIM example usage <serve_llama>`.

Note: NIM can only be run in a Flyte cluster, not locally, as it must be deployed as a sidecar service in a Kubernetes pod.

```{toctree}
:maxdepth: -1
:hidden:

serve_llama
```
