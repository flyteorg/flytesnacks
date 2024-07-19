# %% [markdown]
# (serve_llama)=
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
