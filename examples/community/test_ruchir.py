from typing import Any, Dict, List
from flytekit.testing import patch
from community.ruchir import (
    reports_workflow,
    task1, task2
)


def test_reports_workflow1() -> None:
    x = reports_workflow()
    print(x)


@patch(task1)
@patch(task2)
def test_reports_workflow(task2_mock, task1_mock) -> None:
    reports: List[Dict[str, str]] = [{"messageId": "54321"}]

    # When you send reports as a list instead of a FlytePromise mock, then it fails for >> comparison
    task1_mock.return_value = reports
    task2_mock.return_value = "mocked task 2"

    result = reports_workflow()
    print(result)
    assert result == reports
