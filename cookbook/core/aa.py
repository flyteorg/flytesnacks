import asyncio
import random
import inspect
from pydantic import BaseModel
from contextvars import ContextVar
from typing import Dict, Callable, Any, List
import time
from graphviz import Digraph

current_workflow = ContextVar('current_workflow')


class Person(BaseModel):
    name: str
    height: int
    age: int


class Logger:
    def task_added(self, task):
        print(f"Task {task.name} added to workflow")


class Task:
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.id = id(self)  # id attribute
        self.name = func.__name__
        self.kwargs = {}
        self._result = None

    def __call__(self, **kwargs) -> 'Task':
        self.kwargs = kwargs
        return self

    async def execute(self):
        if self._result is not None:
            return self._result

        for key, value in self.kwargs.items():
            if isinstance(value, Task):
                self.kwargs[key] = await value.execute()
        self._result = self.func(**self.kwargs)
        await asyncio.sleep(3)
        return self._result


class TaskGraph:
    def __init__(self):
        self.graph = Digraph()

    def task_added(self, task):
        self.graph.node(str(task.id), label=task.name)  # use task.id as node name
        for dep_task in task.kwargs.values():
            if isinstance(dep_task, Task):
                self.graph.edge(str(dep_task.id), str(task.id))  # use task.id as node name

    def view(self):
        self.graph.view()


graph = TaskGraph()


class Workflow:
    def __init__(self):
        self.tasks = {}
        self.callbacks = [Logger(), graph]

    def add_task(self, task: Task):
        if task not in self.tasks:
            self.tasks[task] = asyncio.create_task(task.execute())
            for callback in self.callbacks:
                callback.task_added(task)

    async def execute(self):
        await asyncio.gather(*self.tasks.values())

    def get_result(self, task: Task):
        return self.tasks[task].result()


def task(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(**kwargs) -> Task:
        t = Task(func)
        t(**kwargs)
        current_workflow.get().add_task(t)
        return t

    return wrapper


def prompt_task(func: Callable[..., Any]) -> Callable[..., Any]:
    async def async_func(*args, **kwargs):
        return func(*args, **kwargs)

    def wrapper(**kwargs) -> PromptTask:
        pt = PromptTask(async_func)
        pt(**kwargs)
        current_workflow.get().add_task(pt)
        return pt

    return wrapper


def workflow(func: Callable[..., Any]) -> Callable[..., Any]:
    async def wrapper(*args, **kwargs) -> Any:
        wf = Workflow()
        current_workflow.set(wf)
        result = func(*args, **kwargs)
        await wf.execute()
        return wf.get_result(result)

    return wrapper


@task
def return_oldest(p1: Person, p2: Person) -> Person:
    if p1.age > p2.age:
        return p1
    else:
        return p2


@task
def lookup_prompt(name: str) -> Person:
    print(f"Hi {name}")
    return Person(name=name, age=10, height=10)


@workflow
def wf(name: str) -> Task:
    p1 = lookup_prompt(name=name)
    p2 = lookup_prompt(name="yee")
    p3 = return_oldest(p1=p1, p2=p2)
    p4 = lookup_prompt(name="john")
    p5 = return_oldest(p1=p1, p2=p4)
    p5 = return_oldest(p1=p2, p2=p5)
    return p5


await wf(name="evan2")




