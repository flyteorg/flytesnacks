from enum import Enum

from flytekit import task, workflow


class Coffee(Enum):
    ESPRESSO = "espresso"
    AMERICANO = "americano"
    LATTE = "latte"
    CAPPUCCINO = "cappucccino"


@task
def take_order(coffee: str) -> Coffee:
    return Coffee(coffee)


@task
def prep_order(coffee_enum: Coffee) -> str:
    return f"Preparing {coffee_enum.value} ..."


@workflow
def coffee_maker(coffee: str) -> str:
    coffee_enum = take_order(coffee=coffee)
    return prep_order(coffee_enum=coffee_enum)


@workflow
def coffee_maker_enum(coffee_enum: Coffee) -> str:
    return prep_order(coffee_enum=coffee_enum)


if __name__ == "__main__":
    print(coffee_maker(coffee="latte"))
    print(coffee_maker_enum(coffee_enum=Coffee.LATTE))
