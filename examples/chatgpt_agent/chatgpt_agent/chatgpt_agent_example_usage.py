# %% [markdown]
# # ChatGPT agent example usage
#
# ## Basic Example
# ChatGPT can be used in lots of cases, for example, sentiment analysis, language translation, SQL query generation, and text summarization.
#
# This example shows you how to run ChatGPT task in flyte.
#
# %%

from typing import List

import flytekit
from flytekit import ImageSpec, Secret, dynamic, task, workflow
from flytekitplugins.chatgpt import ChatGPTTask

# %% [markdown]
# You have to specify your `name`, `openai organization` and `chatgpt config`.
#
# Name is for flyte and it should be unique.
#
# Openai organization is for openai api, you can find it [here](https://platform.openai.com/account/organization).
#
# Chatgpt config is for openai chat completion, you can find it [here](https://platform.openai.com/docs/api-reference/chat/create).
#
# %%
chatgpt_small_job = ChatGPTTask(
    name="3.5-turbo",
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
    print(f"Running my_chatgpt_job(message='hi') {my_chatgpt_job(message='hi')}")


# %% [markdown]
# ## ChatGPT Summary Bot
# These examples show you the real use case of ChatGPT in the production mode.
#
# For more details, you can refer the [github repository](https://github.com/Future-Outlier/FlyteChatGPTSummaryBot) and the [demo video](https://youtu.be/IS6gi4jR7h0?si=hWHZp5LyjDspiwfD).
# ### Summarize Flyte's Latest Release from GitHub to Slack
#
# %%
flytekit_master = "git+https://github.com/flyteorg/flytekit.git@master"
chatgpt_plugin = "git+https://github.com/flyteorg/flytekit.git@master#subdirectory=plugins/flytekit-openai"
image = ImageSpec(
    apt_packages=["git"],
    packages=[
        flytekit_master,
        chatgpt_plugin,
        "requests",
        "slack_sdk",
    ],
    registry="ghcr.io/flyteorg",
)

chatgpt_job = ChatGPTTask(
    name="3.5-turbo",
    openai_organization="org-NayNG68kGnVXMJ8Ak4PMgQv7",
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)


@task(
    container_image=image,
    secret_requests=[Secret(key="token", group="github-api")],
)
def get_github_latest_release(owner: str = "flyteorg", repo: str = "flyte") -> str:
    import requests

    token = flytekit.current_context().secrets.get("github-api", "token")
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    message = (
        "You are a Bot. Provide a summary of the latest Flyte Github releases for users on Slack."
        "Ensure the response fits within 4000 characters, suitable for a Slack message. "
        "Start the message with 'This is the latest Flyte Github Releases'. "
        f"End the message with 'Checkout the page here: https://github.com/{owner}/{repo}/releases'. "
        "Note: Handling via the Slack API is not required. Format the response in bullet points.\n\n"
        f"Latest Releases:\n{response.json()['body']}"
    )

    return message


@task(
    container_image=image,
    secret_requests=[Secret(key="token", group="slack-api")],
)
def post_message_on_slack(channel: str, message: str):
    from slack_sdk import WebClient

    token = flytekit.current_context().secrets.get("slack-api", "token")
    client = WebClient(token=token)
    client.chat_postMessage(channel=channel, text=message)


@workflow
def wf(owner: str = "flyteorg", repo: str = "flyte", channel: str = "demo"):
    message = get_github_latest_release(owner=owner, repo=repo)
    message = chatgpt_job(message=message)
    post_message_on_slack(channel=channel, message=message)


if __name__ == "__main__":
    wf()


# %% [markdown]
# ### Summarize Flyte's Latest Youtube Video to Slack
# %%
flytekit_master = "git+https://github.com/flyteorg/flytekit.git@master"
chatgpt_plugin = "git+https://github.com/flyteorg/flytekit.git@master#subdirectory=plugins/flytekit-openai"
image = ImageSpec(
    apt_packages=["git"],
    packages=[
        flytekit_master,
        chatgpt_plugin,
        "scrapetube==2.5.1",
        "youtube_transcript_api==0.6.1",
        "slack_sdk==3.23.0",
    ],
    registry="ghcr.io/flyteorg",
)

chatgpt_job = ChatGPTTask(
    name="3.5-turbo",
    openai_organization="org-NayNG68kGnVXMJ8Ak4PMgQv7",
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)


@task(
    container_image=image,
    secret_requests=[Secret(key="token", group="slack-api")],
)
def post_message_on_slack(message: str):
    if message == "":
        return

    from slack_sdk import WebClient

    token = flytekit.current_context().secrets.get("slack-api", "token")
    client = WebClient(token=token)
    client.chat_postMessage(channel="youtube-summary", text=message)


@task(container_image=image)
def get_latest_video_transcript_chunks(channel_url: str) -> List[str]:
    import scrapetube
    from youtube_transcript_api import YouTubeTranscriptApi

    # fetch_latest_video_id
    video_generator = scrapetube.get_channel(channel_url=channel_url)
    latest_video = next(video_generator)
    video_id = latest_video["videoId"]

    # fetch_transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # chunk_transcript
    text_transcript = "\n".join([entry["text"] for entry in transcript])
    return [text_transcript[i : i + 10000] for i in range(0, len(text_transcript), 10000)]


@workflow
def wf(channel_url: str):
    chunks = get_latest_video_transcript_chunks(channel_url=channel_url)
    dynamic_subwf(channel_url=channel_url, chunks=chunks)


@task(container_image=image)
def check_strs_len_less_than_num(msg1: str, msg2: str, num: int) -> bool:
    return len(msg1) + len(msg2) < num


@task(container_image=image)
def concatenate_str(msg1: str, msg2: str) -> str:
    return msg1 + msg2 + "\n"


@task(container_image=image)
def str_is_non_empty(msg: str) -> bool:
    return len(msg) == 0


@dynamic(container_image=image)
def dynamic_subwf(channel_url: str, chunks: List[str]):
    post_message_on_slack(
        message=f"This is the latest video summary, checkout in Flyte's Youtube Channel!\n{channel_url}"
    )

    summary_messages = []
    for chunk in chunks:
        message = chatgpt_job(
            message=concatenate_str(
                msg1=(
                    "Please provide a summary of the following portion of the transcript"
                    " from the latest Flyte YouTube video. Note: This is only a segment"
                    " of the entire transcript, which has been split into multiple parts."
                    " The summary should be concise, not exceeding 4000 characters, and"
                    " suitable for sharing on Slack."
                    "Note: Handling via the Slack API is not required. Format the response in bullet points.\n\n"
                    "Transcript:\n"
                ),
                msg2=chunk,
            )
        )
        summary_messages.append(message)

    message = ""
    for summary_message in summary_messages:
        b = check_strs_len_less_than_num(msg1=message, msg2=summary_message, num=15000)

        if b.is_true:
            message = concatenate_str(msg1=message, msg2=summary_message)

        if b.is_false:
            message = chatgpt_job(
                message=concatenate_str(
                    msg1=(
                        "Please provide a concise summary of the following messages"
                        " generated by ChatGPT. The summary should be suitable for sharing"
                        " on Slack and not exceed 4000 characters."
                        "Note: Handling via the Slack API is not required. Format the response in bullet points.\n\n"
                        "Transcript:\n"
                    ),
                    msg2=message,
                )
            )
            post_message_on_slack(message=message)
            message = summary_message

    b = str_is_non_empty(msg=message)
    if b.is_true:
        message = chatgpt_job(
            message=concatenate_str(
                msg1=(
                    "Please provide a concise summary of the following messages"
                    " generated by ChatGPT. The summary should be suitable for sharing"
                    " on Slack and not exceed 4000 characters."
                    "Note: Handling via the Slack API is not required. Format the response in bullet points.\n\n"
                    "Transcript:\n"
                ),
                msg2=message,
            )
        )
        post_message_on_slack(message=message)


if __name__ == "__main__":
    wf(channel_url="https://www.youtube.com/@flyteorg")

# %% [markdown]
# ### Summarize MLOPs Latest Trend from Medium to Twitter
# Note: This example can only work in the local environment.
# %%
chatgpt_job = ChatGPTTask(
    name="3.5-turbo",
    openai_organization="org-NayNG68kGnVXMJ8Ak4PMgQv7",
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)


@task
def get_weekly_articles_title(url: str = "https://medium.com/tag/flyte") -> str:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    texts = soup.stripped_strings
    all_text = " ".join(texts)

    message = (
        f"You are a Bot. Provide a summary of the latest MLOps trend for users on Medium. "
        f"Your response should fit within 280 characters for a tweet, excluding the article's title. "
        f"Start the message with '''This is the trend of MLOps on Medium this week\n'''. Note: Tweet API handling is not required."
        f"```````"
        f"Article Title: {all_text}"
    )

    return message


@task(
    secret_requests=[
        Secret(key="bearer_token", group="tweet-api"),
        Secret(key="consumer_key", group="tweet-api"),
        Secret(key="consumer_secret", group="tweet-api"),
        Secret(key="access_token", group="tweet-api"),
        Secret(key="access_token_secret", group="tweet-api"),
    ],
)
def tweet(text: str):
    import tweepy

    TWEET_LENGTH = 280
    BEARER_TOKEN = flytekit.current_context().secrets.get("tweet-api", "bearer_token")
    CONSUMER_KEY = flytekit.current_context().secrets.get("tweet-api", "consumer_key")
    CONSUMER_SECRET = flytekit.current_context().secrets.get("tweet-api", "consumer_secret")
    ACCESS_TOKEN = flytekit.current_context().secrets.get("tweet-api", "access_token")
    ACCESS_TOKEN_SECRET = flytekit.current_context().secrets.get("tweet-api", "access_token_secret")

    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    if len(text) > TWEET_LENGTH:
        text = text[:TWEET_LENGTH]
    client.create_tweet(text=text)


@workflow
def wf(url: str = "https://medium.com/tag/flyte"):
    message = get_weekly_articles_title(url=url)
    message = chatgpt_job(message=message)
    tweet(text=message)


if __name__ == "__main__":
    wf()
