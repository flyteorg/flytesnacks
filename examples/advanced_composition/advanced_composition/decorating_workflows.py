# Decorating workflows
from functools import partial, wraps
from unittest.mock import MagicMock

import flytekit
from flytekit import FlyteContextManager, task, workflow
from flytekit.core.node_creation import create_node

# Define the tasks needed for setup and teardown
external_service = MagicMock()


@task
def setup():
    print("initializing external service")
    external_service.initialize(id=flytekit.current_context().execution_id)


@task
def teardown():
    print("finish external service")
    external_service.complete(id=flytekit.current_context().execution_id)


# Create a workflow decorator to wrap the workflow function
def setup_teardown(fn=None, *, before, after):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # get the current flyte context to obtain access to the compilation state of the workflow DAG.
        ctx = FlyteContextManager.current_context()

        # defines before node
        before_node = create_node(before)
        # ctx.compilation_state.nodes == [before_node]

        # under the hood, flytekit compiler defines and threads
        # together nodes within the `my_workflow` function body
        outputs = fn(*args, **kwargs)
        # ctx.compilation_state.nodes == [before_node, *nodes_created_by_fn]

        # defines the after node
        after_node = create_node(after)
        # ctx.compilation_state.nodes == [before_node, *nodes_created_by_fn, after_node]

        # compile the workflow correctly by making sure `before_node`
        # runs before the first workflow node and `after_node`
        # runs after the last workflow node.
        if ctx.compilation_state is not None:
            # ctx.compilation_state.nodes is a list of nodes defined in the
            # order of execution above
            workflow_node0 = ctx.compilation_state.nodes[1]
            workflow_node1 = ctx.compilation_state.nodes[-2]
            before_node >> workflow_node0
            workflow_node1 >> after_node
        return outputs

    if fn is None:
        return partial(setup_teardown, before=before, after=after)

    return wrapper


# Define the DAG
@task
def t1(x: float) -> float:
    return x - 1


@task
def t2(x: float) -> float:
    return x**2


# Create the decorated workflow
@workflow
@setup_teardown(before=setup, after=teardown)
def decorating_workflow(x: float) -> float:
    return t2(x=t1(x=x))


# Run the example locally
if __name__ == "__main__":
    print(decorating_workflow(x=10.0))
