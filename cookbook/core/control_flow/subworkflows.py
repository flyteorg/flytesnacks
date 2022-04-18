import typing
from typing import Tuple
from flytekit import task, workflow, LaunchPlan

op = typing.NamedTuple("OutputsBC", t1_int_output=int, c=str)


@task
def t1(a: int) -> op:
    return op(a + 2, "world")


@workflow
def leaf_subwf(a: int = 42) -> Tuple[str, str]:
    x, y = t1(a=a).with_overrides(node_name="leafwf-n0")
    u, v = t1(a=x).with_overrides(node_name="leafwf-n1")
    return y, v

leaf_lp = LaunchPlan.get_or_create(leaf_subwf)


@workflow
def other_child_wf(a: int = 42) -> Tuple[int, str]:
    x, y = t1(a=a).with_overrides(node_name="other-child-n0")
    return x, y


@workflow
def parent_wf(a: int) -> Tuple[int, str, str]:
    x, y = t1(a=a).with_overrides(node_name="parent-n0")
    u, v = leaf_lp(a=x).with_overrides(node_name="parent-n1")
    return x, u, v


@workflow
def other_parent_wf(a: int) -> Tuple[int, int, str]:
    x, y = t1(a=a).with_overrides(node_name="parent-n0")  # intentionally using the same name
    u, v = other_child_wf(a=x).with_overrides(node_name="parent-n1")  # intentionally using the same name
    return x, u, v


@workflow
def root_level_wf(a: int) -> Tuple[int, str, str, str]:
    x, y = leaf_subwf(a=a).with_overrides(node_name="root-n0")
    m, n, o = parent_wf(a=a).with_overrides(node_name="root-n1")
    return m, n, o, y


@workflow
def other_root_wf(a: int) -> Tuple[int, str, str, int, int, str]:
    x, y, z = parent_wf(a=a).with_overrides(node_name="other-root-n0")
    aa, b, c = other_parent_wf(a=a).with_overrides(node_name="other-root-n1")
    return x, y, z, aa, b, c


# %%
# You can run the nested workflows locally as well.
if __name__ == "__main__":
    print(f"Runnidng root_level_wf(a=3): {root_level_wf(a=3)}")

# hash update 1
