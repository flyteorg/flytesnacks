from pathlib import Path
import flytekit
from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema
from flytekit.types.structured.structured_dataset import StructuredDataset

from typing import List, Dict

# Example of a primitive type task
@task
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b

@workflow
def add_workflow(a: int, b: int) -> int:
    """Workflow to add two integers using the add task.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    # Perform addition and resolve promises
    sum_result = add(a=a, b=b)  # In-memory passing of small data
    return sum_result

# if __name__ == "__main__":
#     print("Add Workflow Result:", add_workflow(a=1, b=2))

# Example of a task processing a list (collection)
@task
def process_list(data: List[int]) -> int:
    """Calculate the sum of a list of integers.

    Args:
        data (List[int]): A list of integers to be summed.

    Returns:
        int: The total sum of the integers in the list.
    """
    return sum(data)

@workflow
def process_list_workflow(data_list: List[int]) -> int:
    """Workflow to process a list of integers using the process_list task.

    Args:
        data_list (List[int]): A list of integers to be summed.

    Returns:
        int: The total sum of the integers in the list.
    """
    return process_list(data=data_list)

# if __name__ == "__main__":
#     print("Process List Workflow Result:", process_list_workflow(data_list=[1, 2, 3]))

# Example of a task processing a dictionary (collection)
@task
def process_dict(data: Dict[str, int]) -> int:
    """Calculate the sum of values in a dictionary.

    Args:
        data (Dict[str, int]): A dictionary where the values are integers.

    Returns:
        int: The total sum of the dictionary values.
    """
    return sum(data.values())

@workflow
def process_dict_workflow(data_dict: Dict[str, int]) -> int:
    """Workflow to process a dictionary of integers using the process_dict task.

    Args:
        data_dict (Dict[str, int]): A dictionary where the values are integers.

    Returns:
        int: The total sum of the dictionary values.
    """
    return process_dict(data=data_dict)

# if __name__ == "__main__":
#     print("Process Dict Workflow Result:", process_dict_workflow(data_dict={"x": 1, "y": 2}))

# Example of a task handling a file (custom type)
@task
def create_file() -> FlyteFile:
    working_dir = Path(flytekit.current_context().working_directory)
    flytefile = working_dir / "test.txt"
    
    # Create the file and write some content (optional)
    with open(flytefile, 'w') as f:
        f.write("This is a test file for Flyte.\n")
    
    return flytefile

@workflow
def create_file_workflow() -> FlyteFile:
    """Workflow to create a file using the create_file task.

    Returns:
        FlyteFile: The created FlyteFile object.
    """
    return create_file()

# if __name__ == "__main__":
#     print("Create File Workflow Result:", create_file_workflow())

# Example of a task handling a StructuredDataset (custom type)
@task
def structured_dataset_task(schema: StructuredDataset) -> str:
    """Process a StructuredDataset and return a confirmation message.

    Args:
        schema (StructuredDataset): The input dataset to be processed.

    Returns:
        str: A message indicating the dataset has been processed.
    """
    return "Structured dataset processed successfully."

@workflow
def structured_task_workflow(schema: FlyteSchema) -> str:
    """Workflow to process a FlyteSchema using the schema_task.

    Args:
        schema (FlyteSchema): The input schema to be processed.

    Returns:
        str: A message indicating the schema has been processed.
    """
    return structured_dataset_task(schema=schema)

# if __name__ == "__main__":
#     # Note: You will need to create a FlyteSchema instance to pass here.
#     # For example purposes, we're assuming a placeholder schema.
#     dummy_schema = FlyteSchema()  # Create an actual FlyteSchema instance as needed
#     print("Schema Task Workflow Result:", schema_task_workflow(schema=dummy_schema))

# Example workflow demonstrating the use of multiple types
@workflow
def combined_workflow(
    a: int,
    b: int,
    data_list: List[int],
    data_dict: Dict[str, int],
    file: FlyteFile
) -> int:
    """Workflow that demonstrates data processing using various types.

    Args:
        a (int): First integer for addition.
        b (int): Second integer for addition.
        data_list (List[int]): List of integers for summation.
        data_dict (Dict[str, int]): Dictionary of integers for summation.
        file (FlyteFile): A file to be processed.

    Returns:
        int: The total sum of all processed values.
    """
    # Perform addition and resolve promises
    sum_result = add(a=a, b=b)  # In-memory passing of small data
    
    # Process list and dictionary, resolving their promises
    list_result = process_list(data=data_list)
    dict_result = process_dict(data=data_dict)
    
    # Process file (not used in the final result)
    file_result = create_file()
    # Data is stored persistently, passing a reference
    # file_result = create_file(file=file)      
    
    # Return the total sum of results, resolving the promises
    return sum_result 
# + list_result + dict_result

if __name__ == "__main__":
    # Uncomment the desired workflow to run
    print("Add Workflow Result:", add_workflow(a=1, b=2))
    print("Process List Workflow Result:", process_list_workflow(data_list=[1, 2, 3]))
    print("Process Dict Workflow Result:", process_dict_workflow(data_dict={"x": 1, "y": 2}))
    print("Create File Workflow Result:", create_file_workflow())
    # To run the schema task, create a dummy schema before calling it
    dummy_schema = FlyteSchema()  # Replace this with an actual schema creation if needed
    print("Schema Task Workflow Result:", structured_task_workflow(schema=dummy_schema))
    print("Combined Workflow Result:", combined_workflow(
        a=1,
        b=2,
        data_list=[1, 2, 3],
        data_dict={"x": 1, "y": 2},
        file=FlyteFile("/tmp/myfile.txt")
    ))