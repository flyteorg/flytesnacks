from typing import Dict, List

from flytekit import task, workflow


@task
def task1() -> List[Dict[str, str]]:
    return [{"messageId": "12345"}]


@task
def task2() -> str:
    return "task2"


@task
def task3() -> str:
    return "task3"


@workflow
def reports_workflow() -> List[Dict[str, str]]:
    output_list = task1()
    output_str_mocked = task2()
    output_str = task3()

    # Change the order of below two lines and the errors will change depending on if mock promise is compared to list
    # or promise is compared to list. Which is why it makes sense to be able to mock output_list response.
    output_list >> output_str_mocked
    output_list >> output_str
    return output_list
