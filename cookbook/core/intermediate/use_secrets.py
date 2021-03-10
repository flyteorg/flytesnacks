"""
Use secrets in a task
----------------------

This example explains how a secret can be accessed in a Flyte Task. Flyte provides different types of Secrets, as part of
SecurityContext. But, for users writing python tasks, you can only access ``secure secrets`` either as environment variable
or injected into a file.

"""
import os
import flytekit

# %%
# Flytekit exposes a type/class called Secrets. It can be imported as follows.
from flytekit import Secret, task

# %%
# Secrets consists of a name and an enum that indicates how the secrets will be accessed. If the mounting_requirement is
# not specified then the secret will be injected as an environment variable is possible. Ideally, you need not worry
# about the mounting requirement, just specify the ``Secret.name`` that matches the declared ``secret`` in Flyte backend
#
# Let us declare a secret named user_secret,

SECRET_NAME = "user_secret"


# %%
# Now declare the secret in the requests. The secret can be accessed using the :py:class:`flytekit.ExecutionParameters`,
# through the global flytekit context as shown in the body of the method
#
# .. note::
#
#   In case of failure to access the secret (it is not found at execution time) an error is raised
@task(secret_requests=[Secret(name=SECRET_NAME)])
def secret_task() -> str:
    secret_val = flytekit.current_context().secrets.get(SECRET_NAME)
    # Please do not print the secret value, we are doing so just as a demonstration
    print(secret_val)
    return secret_val


# %%
# You can use these tasks in your workflow as usual
def my_secret_workflow() -> str:
    return secret_task()


# %%
# Simplest way to test the secret accessibility is to export the secret as an environment variable. There are some
# helper methods available to do so
from flytekit.testing import SecretsManager

if __name__ == "__main__":
    sec = SecretsManager()
    os.environ[sec.get_secrets_env_var(SECRET_NAME)] = "value"
    assert my_secret_workflow() == "value"
