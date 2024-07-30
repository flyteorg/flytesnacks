# %% [markdown]
# (serve_nim_container)=
#
# # Serve Generative AI Models with NIM
#
# This guide demonstrates how to serve a Llama 3 8B model locally with NIM within a Flyte task.
#
# First, instantiate NIM by importing it from the `flytekitplugins.inference` package and specifying the image name along with the necessary secrets.
# The `ngc_image_secret` is required to pull the image from NGC, the `ngc_secret_key` is used to pull models
# from NGC after the container is up and running, and `secrets_prefix` is the environment variable prefix to access {ref}`secrets <secrets>`.
#
# Below is a simple task that serves a Llama NIM container:
# %%
from flytekit import ImageSpec, Resources, Secret, task
from flytekit.extras.accelerators import A10G
from flytekitplugins.inference import NIM, NIMSecrets
from openai import OpenAI

image = ImageSpec(
    name="nim",
    registry="ghcr.io/flyteorg",
    packages=["flytekitplugins-inference"],
)

nim_instance = NIM(
    image="nvcr.io/nim/meta/llama3-8b-instruct:1.0.0",
    secrets=NIMSecrets(
        ngc_image_secret="nvcrio-cred",
        ngc_secret_key="ngc-api-key",
        ngc_secret_group="ngc",
        secrets_prefix="_FSEC_",
    ),
)


@task(
    container_image=image,
    pod_template=nim_instance.pod_template,
    accelerator=A10G,
    secret_requests=[
        Secret(
            group="ngc", key="ngc-api-key", mount_requirement=Secret.MountType.ENV_VAR
        )  # must be mounted as an env var
    ],
    requests=Resources(gpu="0"),
)
def model_serving() -> str:
    client = OpenAI(base_url=f"{nim_instance.base_url}/v1", api_key="nim")  # api key required but ignored

    completion = client.chat.completions.create(
        model="meta/llama3-8b-instruct",
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
# Both chat and chat completion endpoints can be utilized.
#
# You need to mount the secret as an environment variable, as it must be accessed by the `NGC_API_KEY` environment variable within the NIM container.
#
# By default, the NIM instantiation sets `cpu`, `gpu`, and `mem` to `1`, `1`, and `20Gi`, respectively. You can modify these settings as needed.
#
# To serve a fine-tuned Llama model, specify the HuggingFace repo ID in `hf_repo_ids` as `[<your-hf-repo-id>]` and the
# LoRa adapter memory as `lora_adapter_mem`. Set the `NIM_PEFT_SOURCE` environment variable by
# including `env={"NIM_PEFT_SOURCE": "..."}` in the task decorator.
#
# Here is an example initialization for a fine-tuned Llama model:
# %%
nim_instance = NIM(
    image="nvcr.io/nim/meta/llama3-8b-instruct:1.0.0",
    secrets=NIMSecrets(
        ngc_image_secret="nvcrio-cred",
        ngc_secret_key="ngc-api-key",
        ngc_secret_group="ngc",
        secrets_prefix="_FSEC_",
        hf_token_key="hf-key",
        hf_token_group="hf",
    ),
    hf_repo_ids=["<your-hf-repo-id>"],
    lora_adapter_mem="500Mi",
    env={"NIM_PEFT_SOURCE": "/home/nvs/loras"},
)

# %% [markdown]
# :::{note}
# Native directory and NGC support for LoRa adapters coming soon.
# :::
#
# NIM containers can be integrated into different stages of your AI workflow, including data pre-processing,
# model inference, and post-processing. Flyte also allows serving multiple NIM containers simultaneously,
# each with different configurations on various instances.
#
# This integration enables you to self-host and serve optimized AI models on your own infrastructure,
# ensuring full control over costs and data security. By eliminating dependence on third-party APIs for AI model access,
# you gain not only enhanced control but also potentially lower expenses compared to traditional API services.
#
# For more detailed information, refer to the [NIM documentation by NVIDIA](https://docs.nvidia.com/nim/large-language-models/latest/introduction.html).
