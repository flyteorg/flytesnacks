from typing import List, Tuple
import pandas as pd
from flytekit import task, Resources, workflow
from flytekit.types.schema import FlyteSchema


def tower(n, source, destination, auxiliary) -> List[Tuple[int, int]]:
    if n == 1:
        return [(source, destination)]

    results = tower(n - 1, source, auxiliary, destination)
    results.append((source, destination))
    results.extend(tower(n - 1, auxiliary, destination, source))
    return results


@task(requests=Resources(cpu='1', mem="5Gi"), limits=Resources(cpu='1', mem="5Gi"))
def solve_tower(num_discs: int) -> pd.DataFrame:
    results = tower(num_discs, 1, 3, 2)
    df = pd.DataFrame.from_records(results, columns=['From', 'To'])
    return df


@task(requests=Resources(cpu='1', mem="5Gi"), limits=Resources(cpu='1', mem="5Gi"))
def count_rows(steps: FlyteSchema) -> int:
    # Reconstitute the DataFrame
    df = steps.open().all()
    print(df)
    return len(df.index)


@workflow
def tower_wf(discs: int) -> int:
    step_schema = solve_tower(num_discs=discs)
    return count_rows(steps=step_schema)


if __name__ == "__main__":
    print(tower_wf(discs=3))
