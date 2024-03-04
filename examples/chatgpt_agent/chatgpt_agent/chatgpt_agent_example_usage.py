# %% [markdown]
# # ChatGPT agent example usage
#
# This example shows how to use a Flyte ChatGPTTask to execute a task.
# %%

from flytekit import workflow
from flytekitplugins.chatgpt import ChatGPTTask

# %% [markdown]
# You have to specify your name, openai organization and chatgpt config.
#
# Name is for flyte and it should be unique.
#
# Openai organization is for openai api, you can find it [here](https://platform.openai.com/account/organization).
#
# Chatgpt config is for openai chat completion, you can find it [here](https://platform.openai.com/docs/api-reference/chat/create).

# %%
chatgpt_small_job = ChatGPTTask(
    name="gpt-3.5-turbo",
    openai_organization="org-NayNG68kGnVXMJ8Ak4PMgQv7",
    chatgpt_config={
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
    },
)

chatgpt_big_job = ChatGPTTask(
    name="gpt-4",
    openai_organization="org-NayNG68kGnVXMJ8Ak4PMgQv7",
    chatgpt_config={
            "model": "gpt-4",
            "temperature": 0.7,
    },
)

@workflow
def my_chatgpt_job(message: str) -> str:
    message = chatgpt_small_job(message=message)
    message = chatgpt_big_job(message=message)
    return message

# %% [markdown]
# You can execute the workflow locally.
# %%
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running my_chatgpt_job(message='hi') {my_chatgpt_job(message='hi')}"
    )
