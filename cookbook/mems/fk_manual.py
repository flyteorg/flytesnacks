from flytekit.core.context_manager import FlyteContextManager
from flytekit.types.directory import FlyteDirectory
from flytekit.core.type_engine import TypeEngine

target_bucket = "s3://union-oc-production-demo/yt/memtest_fk"

container_dir = "/tmp/flyte-ox9aa6ku/sandbox/local_flytekit/e69fd8f684d1e5f02eadd7f427aeb2d8/test"


fd = FlyteDirectory(container_dir, remote_directory=target_bucket)

ctx = FlyteContextManager.current_context()
lit = TypeEngine.to_literal(ctx, fd, FlyteDirectory, TypeEngine.to_literal_type(FlyteDirectory))
print(lit)
