import inspect


async def f():
    return 123

if __name__ == "__main__":
    inspect.iscoroutinefunction(f)
    coro = f()
    try:
        coro.send(None)
    except StopIteration as e:
        print(f"Answer {e.value}")



