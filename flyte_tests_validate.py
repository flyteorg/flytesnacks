import json
import os
import re
import subprocess

file_list = "flyte_tests.txt"

with open("flyte_tests_manifest.json", "r") as file:
    data = json.load(file)

examples = [(example[0], example[1]) for entry in data for example in entry.get("examples", []) if len(example) >= 1]

for file_name in open(file_list, "r").readlines():
    file_name = file_name.strip()
    print(f"Processing file: {file_name}")

    # Retrieve the file path, including the name of the file and its immediate parent directory
    directory_path = os.path.dirname(file_name).split(os.path.sep)[-1:]
    file_path = ".".join(directory_path + [os.path.splitext(os.path.basename(file_name))[0]])

    # Retrieve the workflow(s)
    workflows = list(filter(lambda tup: file_path in tup[0], examples))

    # Verify if there are any workflows present in the provided file path
    if not workflows:
        raise Exception("The file does not contain any workflows.")

    for workflow, params in workflows:
        # Use the `pyflyte run` command to execute the workflow
        output_string = subprocess.run(["pyflyte", "run", file_name], capture_output=True, text=True).stdout.strip()

        # Define a regular expression pattern to match tasks/workflows in the pyflyte run output
        pattern = re.compile(r"(?<=│ )(\w+)(?=\s+(?:Workflow|Task))")

        # Extract command names using the specified pattern
        commands = re.findall(pattern, output_string)
        print(output_string)
        print(commands)

        # Check if the workflow specified is present in the pyflyte run output
        just_the_workflow = workflow.split(".")[2]

        if just_the_workflow in commands:
            print("Workflow found in the pyflyte run output.")
        else:
            raise Exception("Workflow not found in the pyflyte run output.")

        # Check if the specified parameters are valid
        options_output = subprocess.run(
            ["pyflyte", "run", file_name, just_the_workflow, "--help"], capture_output=True, text=True
        ).stdout

        # Find all matches in the input string
        options = [option.replace("--", "") for option in re.compile(r"--\w+").findall(options_output)]

        # Validate if the provided params are a subset of the supported params
        if set(params).issubset(set(options)):
            print("All parameters found.")
        else:
            raise Exception("There's a mismatch between the values accepted by the workflow and the ones you provided.")
