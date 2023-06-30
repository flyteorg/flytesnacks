from typing import Annotated, List
import typing
from dataclasses import dataclass
import pandas as pd

from flytekit import ImageSpec, task, workflow, kwtypes
from flytekit.types.structured import StructuredDataset


flytekit_pr = ImageSpec(
    packages=["git+https://github.com/flyteorg/flytekit.git@c0f96deb5fe3fc85a2df70c6ac1ae96247edd384"],
    python_version="3.9",
    apt_packages=["git"],
    registry="ghcr.io/unionai-oss",
)


# @dataclass
# class MainParams:
#     region: str
#     preprocess: bool
#     listKeys: List[str]
#
#
# @dataclass
# class ComplexTypes:
#     app_params: MainParams
#     dataset: Annotated[StructuredDataset, kwtypes(column=str)]
#
#
# @task
# def get_df_task() -> Annotated[StructuredDataset, kwtypes(column=str)]:
#     df = pd.DataFrame(dict(column=["foo", "bar"]))
#     return StructuredDataset(df)
#
#
# @task
# def consume(a: ComplexTypes):
#     print(a)
#
#
# @workflow
# def wf():
#     sd = get_df_task()
#     consume(
#         a=ComplexTypes(app_params=MainParams(region="us-west-3", preprocess=False, listKeys=["a", "b"]), dataset=sd)
#     )

"""
   Debug string UNKNOWN:Error received from peer ipv6:%5B::1%5D:30080 {grpc_message:"failed to compile workflow for 
   [resource_type:WORKFLOW project:\"flytesnacks\" domain:\"development\" name:\"cookbook.core.more_dc.wf\" version:
   \"EruwHmATXkejGKWIJa-WmA==\" ] with err failed to compile workflow with err Collected Errors: 3\n\tError 0: Code: 
   MismatchingBindings, Node Id: n1, Description: Input [a] on node [n1] expects bindings of type [].  
   Received [bindings:<key:\"listKeys\" value:<collection:<bindings:<scalar:<primitive:<string_value:\"a\" > > > 
   bindings:<scalar:<primitive:<string_value:\"b\" > > > > > > bindings:<key:\"preprocess\" value:<scalar:<primitive:<boolean:false > > > > 
   bindings:<key:\"region\" value:<scalar:<primitive:<string_value:\"us-west-3\" > > > > ]\n\tError 1: Code: MismatchingTypes, Node Id: n1, 
   Description: Variable [o0] (type [structured_dataset_type:<columns:<name:\"column\" literal_type:<simple:STRING > > > ]) doesn\'t match expected type [].\n\tError 2: Code: ParameterNotBound, Node Id: n1, Description: Parameter not bound [a].\n", grpc_status:13, created_time:"2023-06-21T15:49:42.971189-07:00"}
   dddd
"""


@task
def t21(a: int) -> typing.Tuple[int, str]:
    return a + 2, "world"


@task
def t22(a: typing.Dict[str, str]) -> str:
    return " ".join([v for k, v in a.items()])


@workflow
def wf2(a: int, b: str) -> typing.Tuple[int, str]:
    x, y = t21(a=a)
    d = t22(a={"key1": y, "key2": b})
    return x, d
