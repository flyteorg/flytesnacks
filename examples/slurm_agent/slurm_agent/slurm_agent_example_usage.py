# %% [markdown]
# (slurm_agent_example_usage)=
#
# # Slurm agent example usage 
# The Slurm agent enables seamless integration between Flyte workflows and Slurm-managed high-performance computing (HPC) clusters, allowing users to take advantage of Slurm’s powerful resource allocation, scheduling, and monitoring capabilities.
#
# The following examples demonstrate how to run different types of tasks using the Slurm agent. Let’s start by importing the necessary packages.
# %%
import os

from flytekit import task, workflow
from flytekitplugins.slurm import SlurmFunction 

# %% [markdown]
# ## Slurm Function Task
# `SlurmFunctionTask` is a highly flexible task type that allows you to run a user-defined task function on a Slurm cluster. To configure this task, you need to specify the following fields:
# * `ssh_config`: Options of SSH client connection.
#     * Authentication is done via key pair verification. For available options, please refer to [here](https://github.com/JiangJiaWei1103/flytekit/blob/d0d59d3f809bad89a7567ce49d95c84c3f38bf5f/plugins/flytekit-slurm/flytekitplugins/slurm/ssh_utils.py#L21-L39).
# * `sbatch_conf` (optional): Options of `sbatch` command. If not provided, defaults to an empty dict.
#     * For available options, please refer to the [official Slurm documentation](https://slurm.schedmd.com/sbatch.html).
# * `script` (optional): A user-defined script where `{task.fn}` serves as a placeholder for the task function execution. 
#     * You should insert `{task.fn}` at the desired execution point within the script. If no script is provided, the task function will be executed directly.
# %%
@task(
    task_config=SlurmFunction(
        ssh_config={
            "host": "aws",
            "username": "ubuntu",
            "client_keys": ["~/.ssh/private_key.pem"],
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "tiny-slurm",
            "output": "/home/ubuntu/fn_task.log"
        },
        script="""#!/bin/bash -i

echo [TEST SLURM FN TASK 1] Run the first user-defined task function...

# Setup env vars
export MY_ENV_VAR=123

# Source the virtual env
. /home/ubuntu/.cache/pypoetry/virtualenvs/demo-4A8TrTN7-py3.12/bin/activate 

# Run the user-defined task function
{task.fn}
"""
    )
)
def plus_one(x: int) -> int: 
    print(os.getenv("MY_ENV_VAR"))
    return x + 1


@task(
    task_config=SlurmFunction(
        ssh_config={
            "host": "aws",
            "username": "ubuntu",
        },
        script="""#!/bin/bash -i

echo [TEST SLURM FN TASK 2] Run the second user-defined task function...

. /home/ubuntu/.cache/pypoetry/virtualenvs/demo-4A8TrTN7-py3.12/bin/activate 
{task.fn}
"""
    )
)
def greet(year: int) -> str:
    return f"Hello {year}!!!"


@workflow
def wf(x: int) -> str:
    x = plus_one(x=x)
    msg = greet(year=x)
    return msg


# %% [markdown]
# Finally, you can execute the workflow locally as below:
# %%
if __name__ == "__main__":
    from flytekit.clis.sdk_in_container import pyflyte
    from click.testing import CliRunner

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(f">>> LOCAL EXEC <<<")
    result = runner.invoke(pyflyte.main, ["run", "--raw-output-data-prefix", "s3://my-flyte-slurm-agent", path, "wf", "--x", 2024])
    print(result.output)
