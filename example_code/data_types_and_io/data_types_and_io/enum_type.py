# Enum type
from enum import Enum

from flytekit import task, workflow


# Define an enum and a simple coffee maker workflow that accepts an order
# and brews coffee ☕️ accordingly.
# The assumption is that the coffee maker only understands enum inputs.
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


# The workflow can also accept an enum value
@workflow
def coffee_maker_enum(coffee_enum: Coffee) -> str:
    return prep_order(coffee_enum=coffee_enum)


# You can send a string to the coffee_maker_enum workflow during its execution:
# pyflyte run \
#   https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/data_types_and_io/data_types_and_io/enum_type.py \
#   coffee_maker_enum --coffee_enum="latte"
#
# Run the workflows locally
if __name__ == "__main__":
    print(coffee_maker(coffee="latte"))
    print(coffee_maker_enum(coffee_enum=Coffee.LATTE))
