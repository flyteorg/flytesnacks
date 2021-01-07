from typing import List, Tuple
from flytekit import task


def tower(n, source, destination, auxiliary) -> List[Tuple[int, int]]:
    if n == 1:
        return [(source, destination)]

    results = tower(n - 1, source, auxiliary, destination)
    results.append((source, destination))
    results.extend(tower(n - 1, auxiliary, destination, source))
    return results


@task
def solve_tower(num_discs: int) -> int:
    results = tower(num_discs, 1, 3, 2)
    print(results)
    return len(results)


if __name__ == "__main__":
    print(solve_tower(num_discs=3))
