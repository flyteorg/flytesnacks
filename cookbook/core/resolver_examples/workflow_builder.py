import typing

from flytekit import PythonFunctionTask, workflow


class Builder(object):
    def __init__(self, query):
        self._query = query
        self._process = None
        super().__init__()

    @classmethod
    def read(cls, query):
        return cls(query=query)

    def process(self, fn: typing.Callable):
        self._process = fn
        return self

    def build(self, workflow_name: str):
        @workflow
        def wf_fn():
            t = PythonFunctionTask(task_config=None, task_function=self._process)
            t()

        wf_fn._name = workflow_name

        return wf_fn
