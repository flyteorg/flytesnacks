import typing

import pandas as pd
from flytekit import Workflow, kwtypes, reference_task
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema


@reference_task(
    project="flytesnacks",
    domain="development",
    name="sqlite_datacleaning.tasks.mean_median_imputer",
    version="aedbd6fe44051c171fd966c280c5c3036f658831",
)
def mean_median_imputer(
    dataframe: pd.DataFrame,
    imputation_method: str,
) -> pd.DataFrame:
    ...


@reference_task(
    project="flytesnacks",
    domain="development",
    name="sqlite_datacleaning.tasks.univariate_selection",
    version="aedbd6fe44051c171fd966c280c5c3036f658831",
)
def univariate_selection(
    dataframe: pd.DataFrame,
    split_mask: int,
    num_features: int,
) -> pd.DataFrame:
    ...


wb = Workflow(name="sqlite_datacleaning.workflow.fe_wf")
wb.add_workflow_input("sqlite_archive", FlyteFile[typing.TypeVar("zip")])
wb.add_workflow_input("imputation_method", str)
wb.add_workflow_input("query_template", str)


sql_task = SQLite3Task(
    name="sqlite3.horse_colic",
    query_template=wb.inputs["query_template"],
    inputs=kwtypes(),
    output_schema_type=FlyteSchema,
    task_config=SQLite3Config(
        uri=wb.inputs["sqlite_archive"],
        compressed=True,
    ),
)
node_t1 = wb.add_entity(sql_task)
node_t2 = wb.add_entity(
    mean_median_imputer,
    dataframe=node_t1.outputs["results"],
    imputation_method=wb.inputs["imputation_method"],
)
node_t3 = wb.add_entity(
    univariate_selection,
    dataframe=node_t2.outputs["o0"],
    split_mask=23,
    num_features=15,
)
wb.add_workflow_output(
    "output_from_t3", node_t3.outputs["o0"], python_type=pd.DataFrame
)


if __name__ == "__main__":
    print(
        wb(
            sqlite_archive="https://cdn.discordapp.com/attachments/545481172399030272/852144760273502248/horse_colic.db.zip",
            query_template="select * from data",
            imputation_method="mean",
        )
    )
