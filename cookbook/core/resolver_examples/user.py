from core.resolver_examples.class_builder import Builder
from core.resolver_examples.workflow_builder import Builder as WorkflowBuilder

def get_hello(a: int):
    """
    This mimics a user returning an arbitrary function that needs to run at Task execution time.
    """
    if a == 5:
        def hello() -> str:
            print("Hello from conditional case.")
            return "five"

        return hello

    def hello() -> int:
        print(f"Hello from default case. A was {a}")
        return 42

    return hello


# Using the class based builder
# The `b` here, has to be at the module level because the command that the container ultimately runs with looks like
#   pyflyte-execute --inputs {{.input}} --output-prefix {{.outputPrefix}} \
#     --raw-output-data-prefix {{.rawOutputDataPrefix}} --resolver core.resolver_examples.user.b -- 0
# The "0" at the end means that the builder will use the first task stored in its array of tasks.
# As we discussed during the call, that means that the sequence of things that happen at execution time need to match
# what happens at compilation time.
b = Builder.read("my query").process(get_hello(1))
wf = b.build(workflow_name="user.platform_unique_name_1")


# Using the workflow builder
wf_built_wf = WorkflowBuilder.read("my query").process(get_hello(5)).build(workflow_name="user.platform_unique_name_2")
