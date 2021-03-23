from flytekit import task, workflow
@task
def squared_4(task_1_input: int) -> int:
    sq = task_1_input ** 2
    add_step = sq + 2000
    return add_step
@task
def multiply(task_2_input: int) -> int:
    double = task_2_input * 2 + 3000
    return double
@task
def add(n_1: int, n_2: int) -> int:
    return n_1 + n_2 + 100
@task
def triple(task_3_input: int) -> int:
    return task_3_input * 3
@task
def add_v2(n_1: int, n_2: int) -> int:
    return n_1 + n_2 * 10
@workflow
def computation_workflow(first_number: int, second_number: int) -> int:
    task_1_output = squared_4(task_1_input=first_number)
    task_2_output = multiply(task_2_input=second_number)
    added_numbers = add(n_1=task_1_output, n_2=task_2_output)
    tripled = add_v2(n_1=added_numbers, n_2=added_numbers)
    return tripled
if __name__ == "__main__":
    print(f"Running my_wf() {computation_workflow(first_number=1, second_number=10)}")