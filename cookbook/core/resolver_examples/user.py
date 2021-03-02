
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
