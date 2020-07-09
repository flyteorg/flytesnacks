from __future__ import absolute_import

from flytekit.common import utils
from flytekit.sdk.tasks import inputs
from flytekit.sdk.tasks import outputs
from flytekit.sdk.tasks import python_task
from flytekit.sdk.types import Types

@inputs(
    input_parquet=Types.Schema()
)
@outputs(
    output_csv=Types.MultiPartCSV
)
@python_task(cache_version='sagemaker-3', cache=True, memory_limit="10Gi")
def transform_parquet_to_csv(ctx, input_parquet, output_csv):
    with input_parquet as reader:
        input_parquet_df = reader.read(concat=True)

    with utils.AutoDeletingTempDir("output") as t:
        f = t.get_named_tempfile("output.csv")
        input_parquet_df.to_csv(f, header=False, index=False)
        output_csv.set(t.name)
