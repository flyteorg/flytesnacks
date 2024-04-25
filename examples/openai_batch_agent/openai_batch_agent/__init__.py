from typing import Iterator

from flytekit import workflow
from flytekit.types.file import FlyteFile, JSONLFile
from flytekit.types.iterator import JSON
from flytekitplugins.openai import create_batch


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
def json_iterator_wf(json_vals: Iterator[JSON] = jsons()) -> dict[str, FlyteFile]:
    return batch(jsonl_in=json_vals)


@workflow
def jsonl_wf() -> dict[str, FlyteFile]:
    return batch(jsonl_in=JSONLFile("data.jsonl"))