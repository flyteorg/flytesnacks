from typing import List, Tuple


def tower(n, source, destination, auxiliary) -> List[Tuple[int, int]]:
    if n == 1:
        return [(source, destination)]
    results = tower(n - 1, source, auxiliary, destination)
    results.append((source, destination))
    results.extend(tower(n - 1, auxiliary, destination, source))
    return results


def solve_tower(num_discs: int):
    print(tower(num_discs, 1, 3, 2))


if __name__ == "__main__":
    solve_tower(3)
