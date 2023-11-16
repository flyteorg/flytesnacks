# %% [markdown]
# (attribute_access)=
#
# # Attribute Access
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# Flyte allows users to access attributes directly on output promises for List, Dict, Dataclass, and combinations of them. This allows users to pass attributes of the output directly in workflows, making it more convenient to work with complex data structures.
#
# To begin, import the necessary dependencies and define a common task for later use.
# %%
from dataclasses import dataclass
from typing import Dict, List

from dataclasses_json import dataclass_json
from flytekit import WorkflowFailurePolicy, task, workflow


@task
def print_str(a: str):
    print(a)
    return


# %% [markdown]
# ## List
# We can access the output list by index.
# :::{important}
# Currently, Flyte doesn't support accessing output promises by list slicing
# :::
# %%
@task
def list_task() -> List[str]:
    return ["a", "b"]


@workflow
def list_wf():
    o = list_task()
    print_str(a=o[0])


# %% [markdown]
# You can run the workflow locally.
# %%
if __name__ == "__main__":
    list_wf()

# %% [markdown]
# ## Dict
# We can access the output dict by key.
# %%
@task
def dict_task() -> Dict[str, str]:
    return {"a": "b"}


@workflow
def dict_wf():
    o = dict_task()
    print_str(a=o["a"])


# %% [markdown]
# You can run the workflow locally.
# %%
if __name__ == "__main__":
    dict_wf()

# %% [markdown]
# ## Python Dataclass
# We can also access an attribute of a dataclass.
# %%
@dataclass_json
@dataclass
class foo:
    a: str


@task
def dataclass_task() -> foo:
    return foo(a="b")


@workflow
def dataclass_wf():
    o = dataclass_task()
    print_str(a=o.a)


# %% [markdown]
# You can run the workflow locally.
# %%
if __name__ == "__main__":
    dataclass_wf()

# %% [markdown]
# ## Complex Examples
# The combinations of List, Dict, and Dataclass also work.
# %%
@task
def advance_task() -> (Dict[str, List[str]], List[Dict[str, str]], Dict[str, foo]):
    return {"a": ["b"]}, [{"a": "b"}], {"a": foo(a="b")}


@task
def print_list(a: List[str]):
    print(a)


@task
def print_dict(a: Dict[str, str]):
    print(a)


@workflow
def advanced_workflow():
    dl, ld, dd = advance_task()
    print_str(a=dl["a"][0])
    print_str(a=ld[0]["a"])
    print_str(a=dd["a"].a)

    print_list(a=dl["a"])
    print_dict(a=ld[0])


# %% [markdown]
# You can run the workflow locally.
# %%
if __name__ == "__main__":
    advanced_workflow()


# %% [markdown]
# ## Failed Examples
# The workflows will fail when there is an exception (e.g. out of range).
# %%
@task
def failed_task() -> (List[str], Dict[str, str], foo):
    return ["a", "b"], {"a": "b"}, foo(a="b")


@workflow(
    # The workflow will not fail if one of the nodes encounters an error, as long as there are other nodes that can still be executed.
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE
)
def failed_workflow():
    # This workflow is supposed to fail due to exceptions
    l, d, f = failed_task()
    print_str(a=l[100])
    print_str(a=d["b"])
    print_str(a=f.b)


# %% [markdown]
# failed_workflow should fail.
