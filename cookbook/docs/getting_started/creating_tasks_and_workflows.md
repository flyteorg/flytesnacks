---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(getting_started_creating_tasks_and_workflows)=

# Creating Tasks and Workflows

In the {ref}`Introduction to Flyte <index>`, we got a basic sense of how Flyte
works by creating a few tasks and a simple model-training workflow. In this
guide, you'll learn more about how tasks and workflows fit into the Flyte
programming model.

## 🧱 Tasks

Flyte tasks are the core building blocks of larger, more complex workflows.

### Tasks are Containerized Blocks of Compute

You can think of Flyte tasks as containerized blocks of compute. When tasks are
run in a Flyte backend, they that are actually isolated from all other tasks.
Consider this simple task:

```{code-cell} ipython3
from typing import List
from flytekit import task

@task
def mean(values: List[float]) -> float:
    return sum(values) / len(values)
```

As you can see, a task is just a regular Python function that's decorated
with `@task`. We can run this function just like a function:

```{code-cell} ipython3
mean(values=[float(i) for i in range(1, 11)])
```

```{important}
There are two important things to note here:

- Most of the Flyte tasks you'll ever write can be executed locally.
- Tasks must be invoked with keyword arguments.
```

### Tasks are Strongly Typed

You might also notice that the `mean` function signature is type-annotated with
Python type hints. Flyte uses these annotations to check the input and output
types of the function when it's invoked.

### The Flyte Type System

The Flyte type system uses Python type annotations to make sure that the
data passing through tasks and workflows are compatible with the explicitly
stated types that we define through a function signature.

So if we call the `mean` function with the wrong types, we get an error:

```{code-cell} ipython3
try:
    mean(values="hi")
except Exception as e:
    print(e)
```

This may not seem like much for this simple example, but as you start dealing
with more complex data types and pipelines, Flyte's type system becomes
invaluable for catching bugs early.

Flyte's type system is also used for automatic serialization and deserialization
of data as it's passed from one task to another. You can learn more about it
in the {ref}`User Guide <flyte_type_system>`.

## 🔀 Workflows

Workflows compose multiple tasks – or other workflows – into meaningful steps
of computation to produce some useful set of outputs or outcomes.

Suppose the `mean` task is just one building block of a larger computation.
This is where Flyte workflows can help us manage the added complexity.

### Workflows Build Execution Graphs

Suppose that we want to mean-center and standard-deviation-scale a set of
values. In addition to a `mean` function, we also need to compute standard
deviation and implement the centering and scaling logic.

Let's go ahead and implement those as tasks:

```{code-cell} ipython3
from math import sqrt
from flytekit import workflow


@task
def standard_deviation(values: List[float], mu: float) -> float:
    var = sum([(x - mu) ** 2 for x in values])
    return sqrt(var)

@task
def standard_scale(values: List[float], mu: float, sigma: float) -> List[float]:
    return [(x - mu) / sigma for x in values]
```

Then we put all the pieces together into a workflow:

```{code-cell} ipython3
@workflow
def standard_scale_workflow(values: List[float]) -> List[float]:
    mu = mean(values=values)
    sigma = standard_deviation(values=values, mu=mu)
    return standard_scale(values=values, mu=mu, sigma=sigma) 
```

Just like tasks, workflows are executable in a regular Python runtime:

```{code-cell} ipython3
standard_scale_workflow(values=[float(i) for i in range(1, 11)])
```

```{important}
Although Flyte workflows look like Python code, it's actually a
domain-specific language (DSL) for building execution graphs where tasks
– and other workflows – serve as the building blocks.

This means that the workflow function body only supports a subset of Python's
semantics:

- In workflows, you shouldn't use non-deterministic operations like
  `rand.random`, `time.now()`, etc.
- Within workflows, the outputs of tasks are promises under the hood, so you
  can't access and operate on them like typical Python function outputs. *You
  can only pass promises into other tasks and workflows*.
```

### Promises

A promise is essentially a placeholder for a value that hasn't been
materialized yet. To show you what this means concretely, let's re-define
the workflow above but let's also print the output of one of the tasks:

```{code-cell} ipython3
@workflow
def standard_scale_workflow(values: List[float]) -> List[float]:
    mu = mean(values=values)
    print(mu)  # this is not the actual float value!
    sigma = standard_deviation(values=values, mu=mu)
    return standard_scale(values=values, mu=mu, sigma=sigma) 
```

We didn't even execute the workflow and we're already seeing the value of `mu`,
which is a promise. So what's happening here?

When we decorate `standard_scale_workflow` with `@workflow`, Flyte compiles an
execution graph that's defined inside the function body, *it doesn't actually
run the computations yet*. Therefore, when Flyte compiles a workflow, the
outputs of task calls are actually promises and not regular python values.

### Workflows are Strongly Typed Too

Since both tasks and workflows are strongly typed, Flyte can actually catch
type errors! When we learn about more packaging and registering in the next few
guides, we'll see that Flyte can also catch compile-time errors even before
you running any code!

For now, however, we can run the workflow locally to see that we'll get an
error if we introduce a bug in the `standard_scale` task.

```{code-cell} ipython3
@task
def standard_scale(values: List[float], mu: float, sigma: float) -> float:
    """
    🐞 The implementation and output type of this task is incorrect! It should
    be List[float] instead of a sum of all the scaled values.
    """
    return sum([(x - mu) / sigma for x in values])


@workflow
def standard_scale_workflow(values: List[float]) -> List[float]:
    mu = mean(values=values)
    sigma = standard_deviation(values=values, mu=mu)
    return standard_scale(values=values, mu=mu, sigma=sigma) 

try:
    standard_scale_workflow(values=[float(i) for i in range(1, 11)])
except Exception as e:
    print(e)
```

## What's Next?

So far we've been working with small code snippets and self-contained scripts.
Next, we'll see how to organize a Flyte project that follows software
engineering best practices, including modularizing code into meaningful modules,
defining third-party dependencies, and creating a container image for making
our workflows reproducible.
