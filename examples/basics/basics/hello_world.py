from flytekit import task, workflow


# Define a task that produces the string "Hello, World!"
# by using the `@task` decorator to annotate the Python function
@task
def say_hello() -> str:
    return "Hello, World!"


# Handle the output of a task like that of a regular Python function.
@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res


# Run the workflow locally by calling it like a Python function
if __name__ == "__main__":
    print(f"Running hello_world_wf() {hello_world_wf()}")
