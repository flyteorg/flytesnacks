from flytekit import task


# Task cache serializing is disabled by default to avoid unexpected behavior
# for task executions. To enable use the `cache_serialize` parameter.
# `cache_serialize` is a switch to enable or disable serialization of the task
# This operation is only useful for cacheable tasks, where one may reuse output
# from a previous execution. Flyte requires implicitly enabling the `cache`
# parameter on all cache serializable tasks.
# Cache key definitions follow the same rules as non-serialized cache tasks.
# It is important to understand the implications of the task signature and
# `cache_version` parameter in defining cached results.
@task(cache=True, cache_serialize=True, cache_version="1.0")
def square(n: int) -> int:
    """
     Parameters:
        n (int): name of the parameter for the task will be derived from the name of the input variable.
                 The type will be automatically deduced to Types.Integer

    Return:
        int: The label for the output will be automatically assigned, and the type will be deduced from the annotation

    """
    return n * n
