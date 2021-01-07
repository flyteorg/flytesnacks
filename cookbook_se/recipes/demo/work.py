def tower(n, source, destination, auxiliary):
    if n == 1:
        print(f"({source}, {destination})")
        return
    tower(n - 1, source, auxiliary, destination)
    print(f"({source}, {destination})")
    tower(n - 1, auxiliary, destination, source)


def solve_tower(num_discs: int):
    tower(num_discs, 1, 3, 2)


if __name__ == "__main__":
    solve_tower(3)
