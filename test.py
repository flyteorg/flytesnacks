import re


def get_commands(output):
    # Find lines starting with '|'
    command_lines = re.findall(r"│\s*([a-zA-Z0-9_\-\.]+)\s+", output)

    # Filter out empty strings and 'Commands' line
    commands = [cmd for cmd in command_lines if cmd.lower() != "commands" and cmd.lower() != "--help"]
    return commands


if __name__ == "__main__":
    # Example string output
    example_output = """
    Usage: pyflyte run examples/advanced_composition/advanced_composition/chain_entities.py [OPTIONS] COMMAND [ARGS]...

    Run a [workflow|task] from examples/advanced_composition/advanced_composition/chain_entities.py

    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --help      Show this message and exit.                                                                                                                                             │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ chain_tasks_wf                         Workflow (advanced_composition.chain_entities.chain_tasks_wf)                                                                          │
    │ chain_workflows_wf                     Workflow (advanced_composition.chain_entities.chain_workflows_wf)                                                                      │
    │ sub_workflow_0                         Workflow (advanced_composition.chain_entities.sub_workflow_0)                                                                          │
    │ sub_workflow_1                         Workflow (advanced_composition.chain_entities.sub_workflow_1)                                                                          │
    │ t0                                     Task (advanced_composition.chain_entities.t0)                                                                                          │
    │ t1                                     Task (advanced_composition.chain_entities.t1)                                                                                          │
    │ t2                                     Task (advanced_composition.chain_entities.t2)                                                                                          │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    """

    commands = get_commands(example_output)
    print(commands)
