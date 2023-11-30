import re

s = """
                                                                                
 Usage:                                                                         
 pyflyte run                                                                    
 examples/advanced_composition/advanced_composition/chain_entities.py           
 [OPTIONS] COMMAND [ARGS]...                                                    
                                                                                
 Run a [workflow|task] from                                                     
 examples/advanced_composition/advanced_composition/chain_entities.py           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ chain_tasks_wf      Workflow                                           │
│                     (advanced_composition.chain_entities.chain_tasks_wf)     │
│ chain_workflows_wf  Workflow                                           │
│                     (advanced_composition.chain_entities.chain_workflows_wf) │
│ sub_workflow_0      Workflow                                           │
│                     (advanced_composition.chain_entities.sub_workflow_0)     │
│ sub_workflow_1      Workflow                                           │
│                     (advanced_composition.chain_entities.sub_workflow_1)     │
│ t0                  Task (advanced_composition.chain_entities.t0)      │
│ t1                  Task (advanced_composition.chain_entities.t1)      │
│ t2                  Task (advanced_composition.chain_entities.t2)      │
╰──────────────────────────────────────────────────────────────────────────────╯


"""
# Define a regular expression pattern to match tasks/workflows in the pyflyte run output
pattern = re.compile(r"^\│\s+(\w+)\s+", re.MULTILINE)

# Extract command names using the specified pattern
commands = re.findall(pattern, s)
print(commands)
