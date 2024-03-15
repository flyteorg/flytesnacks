# %% [markdown]
# # FlyteInteractive Jupyter Decorator
#
# The `@jupyter` task decorator launches and monitors a Jupyter notebook server.
# ## Usage
# ### 1. Add the `@jupyter` decorator to a task function definition
# The `@jupyter` decorator takes the following optional parameters:
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
@jupyter
def jupyter_task():
    print("opened notebook")


@workflow
def wf():
    jupyter_task()


if __name__ == "__main__":
    print(wf())

# %% [markdown]
# ### 2. Connect to the Jupyter notebook server
# You can connect in two ways:
# * **(Recommended) Expose a URL on the Flyte console.** Set up ingress on the Flyte backend to expose a URL on the Flyte console. Details are to be determined (TBD).

# * **Use port forwarding.** To use port forwarding, execute the following command:
#    ```
#    $ kubectl port-forward <pod name> <port>
#    ```
#    Then, open a browser and navigate to `localhost:<port>`, replacing `<port>` with the port number configured above. You should be presented with the Jupyter notebook interface.
# %%
