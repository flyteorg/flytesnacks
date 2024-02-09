import flytekit
import pandas
import pandas as pd
from flytekit import ImageSpec, Resources, kwtypes, task, workflow
from flytekit.types.structured.structured_dataset import StructuredDataset
from flytekitplugins.spark import Spark
from flytekit.types.file import FlyteFile

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


custom_image = ImageSpec(name="flyte-spark-plugin2", registry="ghcr.io/katrogan")

@task(
    task_config=Spark(
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
            "spark.jars.packages": "com.acervera.osm4scala:osm4scala-spark3-shaded_2.12:1.0.11",
            "spark.driver.extraJavaOptions": "-Divy.cache.dir=/tmp -Divy.home=/tmp",
        }
    ),
    limits=Resources(mem="2000M"),
    # container_image="ghcr.io/flyteorg/flyte-spark-plugin:bEZhkGOFgC75Vp_JSP1Rug..",
)
def spark_df(pbf_file: FlyteFile) -> pd.DataFrame:
    """
    This task returns a Spark dataset that conforms to the defined schema.
    """
    sess = flytekit.current_context().spark_session
    df = sess.sparkContext.read.format("osm.pbf").load(pbf_file)
    print(f"columns: {df.columns}")
    return df

@workflow
def pois(pbf_file: FlyteFile) -> pd.DataFrame:
    return spark_df(pbf_file=pbf_file)