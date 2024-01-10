# %% [markdown]
# (random_name_workflow)=
#
# # Random name workflow
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# To begin, import the necessary dependencies.
# %%
import random
import string

from flytekit import Workflow, task


def gen_id(size=12, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


@task
def t() -> int:
    return 42


# %% [markdown]
# Generate random name and use imperative style workflow
# %%
wf = Workflow(name=f"basics.random_name_workflow.{gen_id()}")
node_t = wf.add_entity(t)
wf.add_workflow_output("wf_output", node_t.outputs["o0"])
