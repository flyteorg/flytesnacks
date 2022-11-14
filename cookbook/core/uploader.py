from pathlib import Path
from flytekit.types.file import FlyteFile
from flytekit.extend import TypeEngine
from flytekit import FlyteContextManager
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config, DataConfig, S3Config
from flytekit.core.data_persistence import FileAccessProvider

data_config = DataConfig(
    s3=S3Config(endpoint="http://localhost:30002", access_key_id="minio", secret_access_key="miniostorage"))
fa = FileAccessProvider(local_sandbox_dir="/tmp", raw_output_prefix="s3://flyte-sandbox/user-data",
                        data_config=data_config)

def by_type_engine():
    ctx = FlyteContextManager.current_context()
    ff = FlyteFile(path="/Users/ytong/temp/x")
    lit = TypeEngine.to_literal(ctx, ff, FlyteFile, TypeEngine.to_literal_type(FlyteFile))
    print(f"Uploading with settings from the default context {lit}")

    # customized
    ctx = ctx.with_file_access(fa).build()
    lit = TypeEngine.to_literal(ctx, ff, FlyteFile, TypeEngine.to_literal_type(FlyteFile))
    print(f"Uploading with settings {lit}")


def by_manually_calling_fileaccess():
    up = fa.get_random_remote_path()
    fa.upload("/Users/ytong/temp/x", up)
    print(f"Uploaded to {up}")


def by_flyte_remote():
    r = FlyteRemote(
        Config.auto(config_file="/Users/ytong/.flyte/config-sandbox.yaml").with_params(data_config=data_config),
        default_project="flytesnacks",
        default_domain="development",
        data_upload_location="s3://flyte-sandbox/user-data"
    )

    md5, uploaded_location = r._upload_file(Path("/Users/ytong/temp/x"))
    print(f"Remote uploaded to: {uploaded_location}")


def main():
    by_type_engine()
    by_manually_calling_fileaccess()
    by_flyte_remote()


if __name__ == "__main__":
    main()
