def combine_strings(a: str, b: str) -> str:
    return f"{a} {b}"


def hello_world(wf_in1: str, wf_in2: str) -> str:
    return combine_strings(wf_in1, wf_in2)


if __name__ == "__main__":
    print(hello_world("hello", "world"))
