from flytekit import task, workflow


class Superhero:
    def __init__(self, name, power):
        self.name = name
        self.power = power


@task
def welcome_superhero(name: str, power: str) -> Superhero:
    return Superhero(name, power)


@task
def greet_superhero(superhero: Superhero) -> str:
    return f"👋 Hello {superhero.name}! Your superpower is {superhero.power}."


@workflow
def superhero_wf(name: str = "Thor", power: str = "Flight") -> str:
    superhero = welcome_superhero(name=name, power=power)
    return greet_superhero(superhero=superhero)


from typing import Iterator

from flytekit.types.pickle.pickle import BatchSize
from typing_extensions import Annotated


@task
def welcome_superheroes(names: list[str], powers: list[str]) -> Annotated[list[Superhero], BatchSize(3)]:
    return [Superhero(name, power) for name, power in zip(names, powers)]


@task
def greet_superheroes(superheroes: list[Superhero]) -> Iterator[str]:
    for superhero in superheroes:
        yield f"👋 Hello {superhero.name}! Your superpower is {superhero.power}."


@workflow
def superheroes_wf(
    names: list[str] = ["Thor", "Spiderman", "Hulk"],
    powers: list[str] = ["Flight", "Surface clinger", "Shapeshifting"],
) -> Iterator[str]:
    superheroes = welcome_superheroes(names=names, powers=powers)
    return greet_superheroes(superheroes=superheroes)


if __name__ == "__main__":
    print(f"Superhero wf: {superhero_wf()}")
    print(f"Superhero(es) wf: {superheroes_wf()}")
