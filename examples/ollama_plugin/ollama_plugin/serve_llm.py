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

ollama_instance = Ollama(model=Model(name="gemma2"), gpu="1")


@task(
    container_image=image,
    pod_template=ollama_instance.pod_template,
    accelerator=A10G,
    requests=Resources(gpu="0"),
)
def model_serving(user_prompt: str) -> str:
    client = OpenAI(
        base_url=f"{ollama_instance.base_url}/v1", api_key="ollama"
    )  # api key required but ignored

    completion = client.chat.completions.create(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
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
# To serve a fine-tuned model, provide the model configuration within the `Model` dataclass.
# The following parameters are used to configure the model:
#
# - **name**: The name of the model.
# - **mem**: The amount of memory allocated for the model, specified as a string. Default is "500Mi".
# - **cpu**: The number of CPU cores allocated for the model. Default is 1.
# - **from**: The name of an existing model used as a base to create a new custom model.
# - **files**: A list of file names to create the model from.
# - **adapters**: A list of file names to create the model for LORA adapters.
# - **template**: The prompt template for the model.
# - **license**: A string or list of strings containing the license or licenses for the model.
# - **system**: A string containing the system prompt for the model.
# - **parameters**: A dictionary of parameters for the model.
# - **messages**: A list of message objects used to create a conversation.
# - **quantize**: Quantize a non-quantized (e.g. float16) model.
#
# Below is an example of specifying a fine-tuned LoRA adapter for a Llama3 Mario model:
# %%
from flytekit.types.file import FlyteFile

finetuned_ollama_instance = Ollama(
    model=Model(
        name="llama3-mario",
        from_="llama3",
        adapters=["ggml"],
        parameters={"temperature": 1, "num_ctx": 4096},
    ),
    gpu="1",
)


@task(
    container_image=image,
    pod_template=finetuned_ollama_instance.pod_template,
    accelerator=A10G,
    requests=Resources(gpu="0"),
)
def finetuned_model_serving(ggml: FlyteFile): ...


# %% [markdown]
# `ggml` is materialized at run time, with `ggml` available as an input to the task.
# `files` and `adapters` are also materialized during runtime.
#
# Ollama models can be integrated into different stages of your AI workflow, including data pre-processing,
# model inference, and post-processing. Flyte also allows serving multiple Ollama models simultaneously
# on various instances.
#
# This integration enables you to self-host and serve AI models on your own infrastructure,
# ensuring full control over costs and data security.
#
# For more detailed information on the models natively supported by Ollama, visit the [Ollama models library](https://ollama.com/library).
