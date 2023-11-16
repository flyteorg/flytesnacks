import glob
import itertools

directories_to_walk = [
    "examples/basics/basics",
    "examples/data_types_and_io/data_types_and_io",
    "examples/advanced_composition/advanced_composition",
]

all_tests = []
for each_directory in directories_to_walk:
    all_tests.append(glob.glob(f"{each_directory}/*.py"))

print("\n".join(list(itertools.chain(*all_tests))))
