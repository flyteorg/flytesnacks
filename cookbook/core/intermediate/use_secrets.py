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
from flytekit import Secret, task, workflow

# %%
# Secrets consists of a name and an enum that indicates how the secrets will be accessed. If the mounting_requirement is
# not specified then the secret will be injected as an environment variable is possible. Ideally, you need not worry
# about the mounting requirement, just specify the ``Secret.name`` that matches the declared ``secret`` in Flyte backend
#
# Let us declare a secret named user_secret,

SECRET_NAME = "user_secret"
SECRET_GROUP = "user-info"


# %%
# Now declare the secret in the requests. The secret can be accessed using the :py:class:`flytekit.ExecutionParameters`,
# through the global flytekit context as shown in the body of the method
#
# .. note::
#
#   In case of failure to access the secret (it is not found at execution time) an error is raised
@task(secret_requests=[Secret(key=SECRET_NAME, group=SECRET_GROUP)])
def secret_task() -> str:
    secret_val = flytekit.current_context().secrets.get(SECRET_NAME, group=SECRET_GROUP)
    # Please do not print the secret value, we are doing so just as a demonstration
    print(secret_val)
    return secret_val


# %%
# In some cases you may have multiple secrets and sometimes, they maybe grouped as one secret in the SecretStore.
# For example, AWS Secret Manager, has the secret(name, version). Thus in this case the name would be the group, version
# would be the key
# In Kubernetes secrets, it is possible to nest multiple keys under the same secret. Thus in this case the name
# would be the actual name of the nested secret, and the group would be the identifier for the kubernetes secret.
#
# As an example, let us define 2 secrets username and password, defined in the group user_info
USERNAME_SECRET = "username"
PASSWORD_SECRET = "password"


# %%
# The Secret structure allows passing two fields, as described previously matching the key and the group
@task(
    secret_requests=[Secret(key=USERNAME_SECRET, group=SECRET_GROUP), Secret(key=PASSWORD_SECRET, group=SECRET_GROUP)])
def user_info_task() -> (str, str):
    secret_username = flytekit.current_context().secrets.get(USERNAME_SECRET, secrets_group=SECRET_GROUP)
    secret_pwd = flytekit.current_context().secrets.get(PASSWORD_SECRET, secrets_group=SECRET_GROUP)
    # Please do not print the secret value, we are doing so just as a demonstration
    print(f"{secret_username}={secret_pwd}")
    return secret_username, secret_pwd


# %%
# You can use these tasks in your workflow as usual
@workflow
def my_secret_workflow() -> (str, str, str):
    x = secret_task()
    y, z = user_info_task()
    return x, y, z


# %%
# Simplest way to test the secret accessibility is to export the secret as an environment variable. There are some
# helper methods available to do so
from flytekit.testing import SecretsManager

if __name__ == "__main__":
    sec = SecretsManager()
    os.environ[sec.get_secrets_env_var(SECRET_NAME)] = "value"
    os.environ[sec.get_secrets_env_var(USERNAME_SECRET, SECRET_GROUP)] = "username_value"
    os.environ[sec.get_secrets_env_var(PASSWORD_SECRET, SECRET_GROUP)] = "password_value"
    x, y, z = my_secret_workflow()
    assert x == "value"
    assert y == "username_value"
    assert z == "password_value"
