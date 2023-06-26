import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

import asyncio
import random
import inspect
from pydantic import BaseModel
from contextvars import ContextVar
from typing import Dict, Callable, Any, List
import time
from graphviz import Digraph

current_workflow = ContextVar('current_workflow')


class Task:
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.id = id(self)
        self.name = func.__name__
        self.kwargs = {}
        self._result = None

    def __call__(self, **kwargs) -> 'Task':
        self.kwargs = kwargs
        return self

    def __getitem__(self, name):
        return Output(self, name)

    def execute(self, executor):
        if self._result is not None:
            return self._result

        for key, value in self.kwargs.items():
            if isinstance(value, Task):
                self.kwargs[key] = executor.submit(value.execute, executor).result()
            elif isinstance(value, Output):
                task_output = executor.submit(value.task.execute, executor).result()
                self.kwargs[key] = task_output[value.name]

        result = self.func(**self.kwargs)
        if isinstance(result, dict):
            self._result = result
        else:
            self._result = {'output': result}
        return self._result


class Workflow:
    def __init__(self, callbacks=None):
        self.tasks = {}
        self.workflow_result = None  # Track the workflow result
        self.callbacks = callbacks or [Logger()]

    def add_task(self, task: Task):
        if task not in self.tasks:
            self.tasks[task] = task
            for callback in self.callbacks:
                callback.task_added(task)

    def execute(self):
        with ThreadPoolExecutor() as executor:
            for task in self.tasks.keys():
                self.tasks[task] = executor.submit(task.execute, executor)

        # Execute the workflow and store its result
        self.workflow_result = self.get_result(list(self.tasks.keys())[-1]).result()

    def get_result(self, task: Task):
        return self.tasks[task]

    def get_workflow_result(self):
        # Return the result of the workflow
        return self.workflow_result

    def dry_run(self):
        for task in self.tasks.keys():
            task.dry_run()


class Task:
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.id = id(self)
        self.name = func.__name__
        self.kwargs = {}
        self._result = None

    def __call__(self, **kwargs) -> 'Task':
        self.kwargs = kwargs
        return self

    def __getitem__(self, name):
        return Output(self, name)

    def execute_with_dependencies(self, executor: concurrent.futures.Executor):
        # First, resolve any dependencies
        for key, value in list(self.kwargs.items()):
            if isinstance(value, Task):
                if not value._result:
                    value.execute_with_dependencies(executor)
                self.kwargs[key] = value._result
            elif isinstance(value, Output):
                if not value.task._result:
                    value.task.execute_with_dependencies(executor)
                self.kwargs[key] = value.task._result[value.name]

        # Then, execute the task function
        self._result = self.func(**self.kwargs)
        return self._result

    def execute(self):
        if self._result is not None:
            return self._result

        for key, value in self.kwargs.items():
            if isinstance(value, Task):
                self.kwargs[key] = value._result
            elif isinstance(value, Output):
                self.kwargs[key] = value.task._result[value.name]
        self._result = self.func(**self.kwargs)
        return self._result


class Workflow:
    def __init__(self, callbacks=None):
        self.tasks = {}
        self.workflow_result = None
        self.callbacks = callbacks or [Logger()]
        self.threadpool = concurrent.futures.ThreadPoolExecutor()

    def add_task(self, task: Task):
        if task not in self.tasks:
            self.tasks[task] = self.threadpool.submit(task.execute_with_dependencies, self.threadpool)
            for callback in self.callbacks:
                callback.task_added(task)

    def execute(self):
        # Wait for all tasks to complete
        concurrent.futures.wait(self.tasks.values())
        # Retrieve and store the workflow result
        self.workflow_result = self.get_result(list(self.tasks.keys())[-1])

    def get_result(self, task: Task):
        return self.tasks[task].result()

    def get_workflow_result(self):
        return self.workflow_result

    def dry_run(self):
        for task in self.tasks.keys():
            task.dry_run()


def task(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(**kwargs) -> Task:
        t = Task(func)
        t(**kwargs)
        current_workflow.get().add_task(t)
        return t

    return wrapper


def workflow(check_types=False, callbacks=None):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            wf = Workflow(callbacks)
            try:
                current_workflow.get()
            except LookupError:
                # no context has been set yet
                current_workflow.set(wf)
            result = func(*args, **kwargs)
            if check_types:
                wf.dry_run()
            wf.execute()
            return wf.get_workflow_result()

        return wrapper

    return decorator


import time


@task
def lookup_prompt(name: str) -> Person:
    time.sleep(3)
    return name


class Logger:
    def task_added(self, task):
        print(f"Task {task.name} : {task.id} added to workflow")


class TaskGraph:
    def __init__(self):
        self.graph = Digraph()

    def task_added(self, task):
        self.graph.node(str(task.id), label=task.name)
        for dep_task in task.kwargs.values():
            if isinstance(dep_task, Task):
                self.graph.edge(str(dep_task.id), str(task.id))

    def view(self):
        self.graph.view()


graph = TaskGraph()


@workflow(check_types=False, callbacks=[graph])
def wf1() -> Task:
    p1 = lookup_prompt(name="b")
    p2 = lookup_prompt(name=lookup_prompt(name="c"))
    p3 = lookup_prompt(name="a")
    return p3





