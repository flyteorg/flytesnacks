import flytekit

from flytekit import Secret, task, workflow, CronSchedule, LaunchPlan

SECRET_NAME = "user_secret"
SECRET_GROUP = "user-info"


@task(secret_requests=[Secret(group=SECRET_GROUP, key=SECRET_NAME)])
def secret_task() -> str:
    secret_val = flytekit.current_context().secrets.get(SECRET_GROUP, SECRET_NAME)
    # Please do not print the secret value, we are doing so just as a demonstration
    print(secret_val)
    return secret_val


@workflow
def my_secret_workflow() -> str:
    x = secret_task()
    return x


sslp = LaunchPlan.get_or_create(name="scheduled_secrets", workflow=my_secret_workflow,
                                schedule=CronSchedule(schedule="0/1 * * * *"))
