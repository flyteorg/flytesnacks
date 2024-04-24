import json
import re
import subprocess
from pathlib import Path

if __name__ == "__main__":
    file_list = "flyte_tests.txt"

    with open("flyte_tests_manifest.json", "r") as file:
        data = json.load(file)

    examples = [
        (example[0], example[1]) for entry in data for example in entry.get("examples", []) if len(example) >= 1
    ]

    for file_name in open(file_list, "r").readlines():
        file_name = file_name.strip()
        print(f"Processing file: {file_name}")

        # Retrieve the file path, including the name of the file and its immediate parent directory
        file_path = Path(file_name)
        directory_path = file_path.parent.name
        file_name_without_extension = file_path.stem
        import_path = f"{directory_path}.{file_name_without_extension}"

        # Retrieve the workflow(s)
        workflows = list(filter(lambda tup: import_path in tup[0], examples))

        # Verify if there are any workflows present in the provided file path
        if not workflows:
            raise Exception("The file does not contain any workflows.")

        for workflow, params_dict in workflows:
            # Use the `pyflyte run` command to execute the workflow
            output_string = str(subprocess.run(["pyflyte", "run", file_name], capture_output=True, text=True).stdout)

            # Check if the workflow specified is present in the pyflyte run output
            cleaned_string = re.sub(r"\x1b\[[0-9;]*[mG]", "", output_string)
            just_the_workflow = workflow.split(".")[2]
            if just_the_workflow in cleaned_string.split():
                print("Workflow found in the pyflyte run output.")
            else:
                raise Exception("Workflow not found in the pyflyte run output.")

            # Check if the specified parameters are valid
            options_output = subprocess.run(
                ["pyflyte", "run", file_name, just_the_workflow, "--help"],
                capture_output=True,
                text=True,
            ).stdout

            params = params_dict.keys()
            if not params:
                print("No parameters found.")
            elif any(re.findall(r"|".join(params), options_output, re.IGNORECASE)):
                print("All parameters found.")
            else:
                raise Exception(
                    "There's a mismatch between the values accepted by the workflow and the ones you provided."
                )
