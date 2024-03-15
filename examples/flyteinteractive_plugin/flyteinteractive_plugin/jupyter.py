# %% [markdown]
# # FlyteInteractive Jupyter Decorator
#
# The `@jupyter` task decorator launches and monitors a Jupyter notebook server.
# ## Usage
# Add the `@jupyter` decorator to a task function definition.
# This decorator takes the following optional parameters:
# * **max_idle_seconds:** Optional[int] (default 36000)
# * **port:** Optional[int] (default 8888)
# * **enable:** Optional[bool] (default True)
# * **notebook_dir:** Optional[str] (default "/root")
# * **pre_execute:** Optional[Callable] (default None)
# * **post_execute:** Optional[Callable], (default None)
# %%

from flytekit import task, workflow
from flytekitplugins.flyteinteractive import jupyter


@task
@jupyter()
def jupyter_task():
    print("opened notebook")


@workflow
def wf():
    jupyter_task()


if __name__ == "__main__":
    print(wf())
