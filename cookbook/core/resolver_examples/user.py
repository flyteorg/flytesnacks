from core.resolver_examples.class_builder import Builder


def get_hello(a: int):
    """
    This mimics a user returning an arbitrary function that needs to run at Task execution time.
    """
    if a == 5:
        def hello() -> int:
            print("hello")
            return 5

        return hello

    def hello() -> int:
        print(f"Hello, A was {a}")
        return 42

    return hello


# Using the class based builder
b = Builder.read("my query").process(get_hello(1))
wf = b.build(workflow_name="user.platform_unique_name_1")
