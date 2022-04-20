import pandas as pd

from flytekit import task, workflow, kwtypes
from flytekit.types.structured.structured_dataset import (
    StructuredDataset,
)

from typing_extensions import Annotated


superset_cols = kwtypes(name=str, age=int)
subset_cols = kwtypes(age=int)


@task
def get_subset_df(
    df: Annotated[pd.DataFrame, superset_cols]
) -> Annotated[StructuredDataset, subset_cols]:
    df = pd.concat([df, pd.DataFrame([[30]], columns=["age"])])
    return StructuredDataset(dataframe=df)


@task
def show_sd(in_sd: StructuredDataset):
    pd.set_option('expand_frame_repr', False)
    df = in_sd.open(pd.DataFrame).all()
    print(df)


@workflow
def my_wf(remote: pd.DataFrame, image: StructuredDataset) -> Annotated[StructuredDataset, subset_cols]:
    x = get_subset_df(
        df=remote
    )  # noqa: shown for demonstration; users should use the same types between tasks
    print(f"|{x}|")
    show_sd(in_sd=x)
    show_sd(in_sd=image)
    return x
