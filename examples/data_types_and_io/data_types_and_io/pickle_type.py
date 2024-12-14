from flytekit import task, workflow


# `Superhero` represents a user-defined complex type that can be serialized
# to a pickle file by Flytekit
# and transferred between tasks as both input and output data.
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


# Run the workflow locally
if __name__ == "__main__":
    print(f"Superhero wf: {superhero_wf()}")
