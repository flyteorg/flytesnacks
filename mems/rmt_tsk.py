from flytekit import task
from flytekit.types.file import FlyteFile

@task
def my_task(input: str) -> FlyteFile:
    fn = 'out.txt'
    with open(fn, "w") as f:
        f.write(input)
    ff = FlyteFile(path=fn)
    return ff

