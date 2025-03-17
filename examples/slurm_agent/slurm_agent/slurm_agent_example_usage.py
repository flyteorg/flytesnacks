# %% [markdown]
# (slurm_agent_example_usage)=
#
# # Slurm agent example usage
# The Slurm agent enables seamless integration between Flyte workflows and Slurm-managed high-performance computing (HPC) clusters, allowing users to take advantage of Slurm’s powerful resource allocation, scheduling, and monitoring capabilities.
#
# The following examples demonstrate how to run different types of tasks using the Slurm agent, covering both basic and advanced use cases. Let’s start by importing the necessary packages.
# %%
import os

from flytekit import task, workflow
from flytekitplugins.slurm import Slurm, SlurmFunction, SlurmRemoteScript, SlurmShellTask, SlurmTask

# %% [markdown]
# ## `SlurmTask`
# First, `SlurmTask` is the most basic use case, allowing users to directly run a pre-existing shell script on the Slurm cluster. To configure this task, you need to specify the following fields:
# * `ssh_config`: Options of SSH client connection.
#     * Authentication is done via key pair verification. For available options, please refer to [here](https://github.com/JiangJiaWei1103/flytekit/blob/d0d59d3f809bad89a7567ce49d95c84c3f38bf5f/plugins/flytekit-slurm/flytekitplugins/slurm/ssh_utils.py#L21-L39).
# * `batch_script_path`: Path to the shell script on the Slurm cluster.
# * `sbatch_conf` (optional): Options of `sbatch` command. If not provided, defaults to an empty dict.
#     * For available options, please refer to the [official Slurm documentation](https://slurm.schedmd.com/sbatch.html).
# * `batch_script_args` (optional): Additional arguments for the batch script on Slurm cluster.
# %%
slurm_task = SlurmTask(
    name="basic",
    task_config=SlurmRemoteScript(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "job0",
        },
        batch_script_path="/home/ubuntu/echo.sh",
    ),
)


@workflow
def wf() -> None:
    slurm_task()


# %% [markdown]
# Then, you can execute the workflow locally as below:
# %%
if __name__ == "__main__":
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(">>> LOCAL EXEC <<<")
    result = runner.invoke(pyflyte.main, ["run", path, "wf"])
    print(result.output)


# %% [markdown]
# ## `SlurmShellTask`
# Instead of running a pre-existing shell script on the Slurm cluster, `SlurmShellTask` allows users to define the script content within the interface as shown below:
# %%
shell_task = SlurmShellTask(
    name="shell",
    script="""#!/bin/bash -i

echo [TEST SLURM SHELL TASK 1] Run the user-defined script...
""",
    task_config=Slurm(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
            "client_keys": ["~/.ssh/private_key.pem"],
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "job1",
        },
    ),
)


shell_task_with_args = SlurmShellTask(
    name="shell",
    script="""#!/bin/bash -i

echo [TEST SLURM SHELL TASK 2] Run the user-defined script with args...
echo Arg1: $1
echo Arg2: $2
echo Arg3: $3
""",
    task_config=Slurm(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
        },
        sbatch_conf={
            "partition": "debug",
            "job-name": "job2",
        },
        batch_script_args=["0", "a", "xyz"],
    ),
)


@workflow
def wf() -> None:
    shell_task()
    shell_task_with_args()


# %% [markdown]
# Once again, execute the workflow locally to view the results:
# %%
if __name__ == "__main__":
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(">>> LOCAL EXEC <<<")
    result = runner.invoke(pyflyte.main, ["run", path, "wf"])
    print(result.output)


# %% [markdown]
# ## `SlurmFunctionTask`
# Finally, `SlurmFunctionTask` is a highly flexible task type that allows you to run a user-defined task function on a Slurm cluster. To configure this task, you need to specify the following fields:
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
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
            "client_keys": ["~/.ssh/private_key.pem"],
        },
        sbatch_conf={"partition": "debug", "job-name": "job3", "output": "/home/ubuntu/fn_task.log"},
        script="""#!/bin/bash -i

echo [TEST SLURM FN TASK 1] Run the first user-defined task function...

# Setup env vars
export MY_ENV_VAR=123

# Source the virtual env
. /home/ubuntu/.cache/pypoetry/virtualenvs/demo-4A8TrTN7-py3.12/bin/activate

# Run the user-defined task function
{task.fn}
""",
    )
)
def plus_one(x: int) -> int:
    print(os.getenv("MY_ENV_VAR"))
    return x + 1


@task(
    task_config=SlurmFunction(
        ssh_config={
            "host": "ec2-11-22-33-444.us-west-2.compute.amazonaws.com",
            "username": "ubuntu",
        },
        script="""#!/bin/bash -i

echo [TEST SLURM FN TASK 2] Run the second user-defined task function...

. /home/ubuntu/.cache/pypoetry/virtualenvs/demo-4A8TrTN7-py3.12/bin/activate
{task.fn}
""",
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
# Let's execute the workflow:
# %%
if __name__ == "__main__":
    from click.testing import CliRunner
    from flytekit.clis.sdk_in_container import pyflyte

    runner = CliRunner()
    path = os.path.realpath(__file__)

    print(">>> LOCAL EXEC <<<")
    result = runner.invoke(
        pyflyte.main, ["run", "--raw-output-data-prefix", "s3://my-flyte-slurm-agent", path, "wf", "--x", 2024]
    )
    print(result.output)
