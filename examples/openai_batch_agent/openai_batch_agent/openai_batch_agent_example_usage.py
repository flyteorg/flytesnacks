# %% [markdown]
# (openai_batch_agent_example_usage)=
#
# # Batching Requests for Asynchronous Processing
#
# This example demonstrates how to send a batch of API requests to GPT models for asynchronous processing.
#
# Every batch input should include `custom_id`, `method`, `url`, and `body`.
# You can provide either a `JSONLFile` or `Iterator[JSON]`, and the agent handles the file upload to OpenAI,
# creation of the batch, and downloading of the output and error files.
#
# ## Using `Iterator`
#
# Here's how you can provide an `Iterator` as an input to the agent:
# %%
from typing import Iterator

from flytekit import workflow
from flytekit.types.file import JSONLFile
from flytekit.types.iterator import JSON
from flytekitplugins.openai import BatchResult, create_batch


def jsons():
    for x in [
        {
            "custom_id": "request-1",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is 2+2?"},
                ],
            },
        },
        {
            "custom_id": "request-2",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Who won the world series in 2020?"},
                ],
            },
        },
    ]:
        yield x


batch = create_batch(
    name="gpt-3.5-turbo",
    openai_organization="your-org",
)


@workflow
def json_iterator_wf(json_vals: Iterator[JSON] = jsons()) -> BatchResult:
    return batch(jsonl_in=json_vals)


# %% [markdown]
# The `create_batch` function returns an imperative workflow responsible for uploading the JSON data to OpenAI,
# creating a batch, polling the status of the batch to check for completion, and downloading the
# output and error files. It also accepts a `config` parameter, allowing you to provide `metadata`, `endpoint`,
# and `completion_window` values. These parameters default to their respective default values.
#
# `BatchResult` is a `NamedTuple` that contains the paths to the output file and the error file.
#
# ## Using `JSONLFile`
#
# The following code snippet demonstrates how to send a JSONL file to the `create_batch` function:
# %%
@workflow
def jsonl_wf() -> BatchResult:
    return batch(jsonl_in=JSONLFile("data.jsonl"))


# %% [markdown]
# The iterator streams JSONs to reduce the memory footprint. If you have large batches of requests that are huge in size,
# you can leverage the iterator. It streams the data to a JSONL file and uploads it to OpenAI, whereas `JSONLFile`
# downloads the file in its entirety at once and uploads it to OpenAI.
#
# You can find more info about the [Batch API in the OpenAI docs](https://help.openai.com/en/articles/9197833-batch-api-faq).