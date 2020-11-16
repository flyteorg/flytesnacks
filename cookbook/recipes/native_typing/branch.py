# import typing

# from flytekit.annotated.task import task
# from flytekit.annotated.workflow import workflow
# from flytekit.annotated.condition import conditional

# @task
# def mimic(a: int) -> typing.NamedTuple("OutputsBC", c=int):
#     return a

# @task
# def t1() -> typing.NamedTuple("OutputsBC", c=str):
#     return "world"

# @task
# def t2() -> typing.NamedTuple("OutputsBC", c=str):
#     return "hello"

# @workflow
# def my_wf(a: int) -> str:
#     c = mimic(a=a)
#     return (conditional("test1")
#             .if_(c == 4)
#             .then(t1())
#             .else_()
#             .then(t2())
#             )


# if __name__ == "__main__":
#     print(my_wf(a=4))
#     print(my_wf(a=2))
