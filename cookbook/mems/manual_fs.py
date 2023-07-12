import fsspec

target_bucket = "s3://union-oc-production-demo/yt/memtest1"

container_dir = "/tmp/flyte-ox9aa6ku/sandbox/local_flytekit/e69fd8f684d1e5f02eadd7f427aeb2d8/test"
fs = fsspec.filesystem("s3")

fs.put(container_dir, target_bucket, recursive=True)

