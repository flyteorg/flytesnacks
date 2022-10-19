from flytekit import task, workflow

@task
def or_operation(a: bool, b: bool) -> bool:
    return a or b

@workflow
def wf(a: bool, b: bool) -> bool:
    return or_operation(a=a, b=b)

if __name__ == "__main__":
    print(wf(a=True, b=False))