import os
from typing import Tuple

import flytekit
from flytekit import Secret, task, workflow
from flytekit.testing import SecretsManager

# Flyte supports running a variety of tasks, from containers to SQL queries and
# service calls, and it provides a native Secret construct to request and access
# secrets.
#
# This example explains how you can access secrets in a Flyte Task. Flyte provides
# different types of secrets, but for users writing Python tasks, you can only access
# secure secrets either as environment variables or as a file injected into the
# running container.


# Prerequisites:
# - Install [kubectl](https://kubernetes.io/docs/tasks/tools/).
# - Have access to a Flyte cluster, for e.g. with `flytectl demo start` as
#   described in
#   https://docs.flyte.org/en/latest/getting_started_with_workflow_development/running_a_workflow_locally.html#running-a-workflow-in-a-local-flyte-cluster


# The first step to using secrets in Flyte is to create one on the backend.
# By default, Flyte uses the K8s-native secrets manager, which we'll use in this
# example, but you can also {ref}`configure different secret managers <configure_secret_management>`.
#
# First, we use `kubectl` to create a secret called `user-info` with a
# `user_secret` key:
#    kubectl create secret -n <project>-<domain> generic user-info --from-literal=user_secret=mysecret

# Be sure to specify the correct Kubernetes namespace when creating a secret. If you plan on accessing
# the secret in the `flytesnacks` project under the `development` domain, replace `<project>-<domain>`
# with `flytesnacks-development`. This is because secrets need to be in the same namespace as the
# workflow execution.


# The imperative command above is useful for creating secrets in an ad hoc manner,
# but it may not be the most secure or sustainable way to do so. You can, however,
# define secrets using a [configuration file](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-config-file/)
# or tools like [Kustomize](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kustomize/).


# Once you've defined a secret on the Flyte backend, `flytekit` exposes a class
# called `flytekit.Secret`s, which allows you to request a secret
# from the configured secret manager.

secret = Secret(
    group="<SECRET_GROUP>",
    key="<SECRET_KEY>",
    mount_requirement=Secret.MountType.ENV_VAR,
)


# Secrets consists of `group`, `key`, and `mounting_requirement` arguments,
# where a secret group can have multiple secrets associated with it.
# If the `mounting_requirement` argument is not specified, the secret will
# be injected as an environment variable by default.
#
# In the code below we specify two variables, `SECRET_GROUP` and
# `SECRET_NAME`, which maps onto the `user-info` secret that we created
# with `kubectl` above, with a key called `user_secret`.


SECRET_GROUP = "user-info"
SECRET_NAME = "user_secret"


# Now we declare the secret in the `secret_requests` argument of the
# `@task` decorator. The request tells Flyte to make
# the secret available to the task.

# The secret can then be accessed inside the task using the
# `flytekit.ExecutionParameters` object, which is returned by
# invoking the `flytekit.current_context` function, as shown below.

# At runtime, flytekit looks inside the task pod for an environment variable or
# a mounted file with a predefined name/path and loads the value.


@task(secret_requests=[Secret(group=SECRET_GROUP, key=SECRET_NAME)])
def secret_task() -> str:
    context = flytekit.current_context()
    secret_val = context.secrets.get(SECRET_GROUP, SECRET_NAME)
    print(secret_val)
    return secret_val


# WARNING: Never print secret values! The example above is just for demonstration purposes.

# In some cases you may have multiple secrets and sometimes, they maybe grouped
# as one secret in the SecretStore.
#
# For example, In Kubernetes secrets, it is possible to nest multiple keys under
# the same secret:

#    kubectl create secret generic user-info \
#        --from-literal=user_secret=mysecret \
#        --from-literal=username=my_username \
#        --from-literal=password=my_password

# In this case, the secret group will be `user-info`, with three available
# secret keys: `user_secret`, `username`, and `password`.


USERNAME_SECRET = "username"
PASSWORD_SECRET = "password"


# The Secret structure allows passing two fields,
# matching the key and the group, as previously described:
@task(
    secret_requests=[
        Secret(key=USERNAME_SECRET, group=SECRET_GROUP),
        Secret(key=PASSWORD_SECRET, group=SECRET_GROUP),
    ]
)
def user_info_task() -> Tuple[str, str]:
    context = flytekit.current_context()
    secret_username = context.secrets.get(SECRET_GROUP, USERNAME_SECRET)
    secret_pwd = context.secrets.get(SECRET_GROUP, PASSWORD_SECRET)
    print(f"{secret_username}={secret_pwd}")
    return secret_username, secret_pwd


# WARNING: Never print secret values! The example above is just for demonstration purposes.


# It is possible to make Flyte mount the secret as a file or an environment
# variable.

# The file type is useful for large secrets that do not fit in environment variables,
# which are typically asymmetric keys (like certs, etc). Another reason may be that a
# dependent library requires the secret to be available as a file.
# In these scenarios you can specify the `mount_requirement=Secret.MountType.FILE`.


# In the following example we force the mounting to be an environment variable:
@task(
    secret_requests=[
        Secret(
            group=SECRET_GROUP,
            key=SECRET_NAME,
            mount_requirement=Secret.MountType.ENV_VAR,
        )
    ]
)
def secret_file_task() -> Tuple[str, str]:
    secret_manager = flytekit.current_context().secrets

    # get the secrets filename
    f = secret_manager.get_secrets_file(SECRET_GROUP, SECRET_NAME)

    # get secret value from an environment variable
    secret_val = secret_manager.get(SECRET_GROUP, SECRET_NAME)

    # returning the filename and the secret_val
    return f, secret_val


# These tasks can be used in your workflow as usual
@workflow
def my_secret_workflow() -> Tuple[str, str, str, str, str]:
    x = secret_task()
    y, z = user_info_task()
    f, s = secret_file_task()
    return x, y, z, f, s


# The simplest way to test secret accessibility is to export the secret as an
# environment variable. There are some helper methods available to do so:
if __name__ == "__main__":
    sec = SecretsManager()
    os.environ[sec.get_secrets_env_var(SECRET_GROUP, SECRET_NAME)] = "value"
    os.environ[sec.get_secrets_env_var(SECRET_GROUP, USERNAME_SECRET)] = "username_value"
    os.environ[sec.get_secrets_env_var(SECRET_GROUP, PASSWORD_SECRET)] = "password_value"
    x, y, z, f, s = my_secret_workflow()
    assert x == "value"
    assert y == "username_value"
    assert z == "password_value"
    assert f == sec.get_secrets_file(SECRET_GROUP, SECRET_NAME)
    assert s == "value"
