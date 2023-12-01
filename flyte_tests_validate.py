import json
import os
import re
import subprocess

file_list = "flyte_tests.txt"

with open("flyte_tests_manifest.json", "r") as file:
    data = json.load(file)

examples = [(example[0], example[1]) for entry in data for example in entry.get("examples", []) if len(example) >= 1]


def get_commands(output):
    # Find lines starting with '|'
    command_lines = re.findall(r"│\s*([a-zA-Z0-9_\-\.]+)\s+", output)

    # Filter out 'Commands' and "--help" lines
    commands = [cmd for cmd in command_lines if cmd.lower() != "commands" and cmd.lower() != "--help"]
    return commands


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

    for workflow, params_dict in workflows:
        # Use the `pyflyte run` command to execute the workflow
        output_string = str(subprocess.run(["pyflyte", "run", file_name], capture_output=True, text=True).stdout)

        # Check if the workflow specified is present in the pyflyte run output
        print(output_string.split())
        just_the_workflow = workflow.split(".")[2]
        if just_the_workflow in output_string.split():
            print("Workflow found in the pyflyte run output.")
        else:
            raise Exception("Workflow not found in the pyflyte run output.")

        # Check if the specified parameters are valid
        options_output = subprocess.run(
            ["pyflyte", "run", file_name, just_the_workflow, "--help"],
            capture_output=True,
            text=True,
        ).stdout

        # Find all matches in the input string
        params = params_dict.keys()
        if not params:
            print("No parameters found.")
        elif any(re.findall(r"|".join(params), options_output, re.IGNORECASE)):
            print("All parameters found.")
        else:
            raise Exception("There's a mismatch between the values accepted by the workflow and the ones you provided.")
