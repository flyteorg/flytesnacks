# %% [markdown]
# (serve_llm)=
#
# # Serve LLMs with Ollama
#
# In this guide, you'll learn how to locally serve Gemma2 and fine-tuned Llama3 models using Ollama within a Flyte task.
#
# Start by importing Ollama from the `flytekitplugins.inference` package and specifying the desired model name.
#
# Below is a straightforward example of serving a Gemma2 model:
# %%
from flytekit import ImageSpec, Resources, task
from flytekit.extras.accelerators import A10G
from flytekitplugins.inference import Model, Ollama
from openai import OpenAI

image = ImageSpec(
    name="ollama_serve",
    registry="ghcr.io/flyteorg",
    packages=["flytekitplugins-inference"],
    builder="default",
)

ollama_instance = Ollama(model=Model(name="gemma2"))


@task(
    container_image=image,
    pod_template=ollama_instance.pod_template,
    accelerator=A10G,
    requests=Resources(gpu="0"),
)
def model_serving() -> str:
    client = OpenAI(base_url=f"{ollama_instance.base_url}/v1", api_key="ollama")  # api key required but ignored

    completion = client.chat.completions.create(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": "Write a limerick about the wonders of GPU computing.",
            }
        ],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
    )

    return completion.choices[0].message.content


# %% [markdown]
# :::{important}
# Replace `ghcr.io/flyteorg` with a container registry to which you can publish.
# To upload the image to the local registry in the demo cluster, indicate the registry as `localhost:30000`.
# :::
#
# The `model_serving` task initiates a sidecar service to serve the model, making it accessible on localhost via the `base_url` property.
# You can use either the chat or chat completion endpoints.
#
# By default, Ollama initializes the server with `cpu`, `gpu`, and `mem` set to `1`, `1`, and `15Gi`, respectively.
# You can adjust these settings to meet your requirements.
#
# To serve a fine-tuned model, provide the model configuration as `modelfile` within the `Model` dataclass.
#
# Below is an example of specifying a fine-tuned LoRA adapter for a Llama3 Mario model:
# %%
from flytekit.types.file import FlyteFile

finetuned_ollama_instance = Ollama(
    model=Model(
        name="llama3-mario",
        modelfile="FROM llama3\nADAPTER {inputs.ggml}\nPARAMETER temperature 1\nPARAMETER num_ctx 4096\nSYSTEM {inputs.system_prompt}",
    )
)


@task(
    container_image=image,
    pod_template=finetuned_ollama_instance.pod_template,
    accelerator=A10G,
    requests=Resources(gpu="0"),
)
def finetuned_model_serving(ggml: FlyteFile, system_prompt: str) -> str:
    ...


# %% [markdown]
# `{inputs.ggml}` and `{inputs.system_prompt}` are materialized at run time, with `ggml` and `system_prompt` available as inputs to the task.
#
# Ollama models can be integrated into different stages of your AI workflow, including data pre-processing,
# model inference, and post-processing. Flyte also allows serving multiple Ollama models simultaneously
# on various instances.
#
# This integration enables you to self-host and serve AI models on your own infrastructure,
# ensuring full control over costs and data security.
#
# For more detailed information on the models natively supported by Ollama, visit the [Ollama models library](https://ollama.com/library).
