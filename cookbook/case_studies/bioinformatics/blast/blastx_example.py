"""
BLASTX Example
--------------

In this example, we will use BLASTX to search for a nucleotide sequence against a local protein database.
"""

# %%
# First, we need to import some libraries.
import os
from typing import Tuple, NamedTuple

import matplotlib.pyplot as plt
import pandas as pd

# import Biopython tools for running local BLASTX
from Bio.Blast.Applications import NcbiblastxCommandline
from flytekit import conditional, kwtypes, task, workflow
from flytekit.extras.tasks.shell import OutputLocation, ShellTask
from flytekit.types.file import FlyteFile, PNGImageFile

# %%
# We define a task to generate BLASTX command using `NcbiblastxCommandline <https://biopython.org/docs/1.75/api/Bio.Blast.Applications.html#Bio.Blast.Applications.NcbiblastpCommandline>`__.
# We provide the location of the database, the location of the query sequence, the output location, and ``outfmt`` as arguments.
#
# .. note::
#   ``outfmt=6`` asks BLASTX to write a tab-separated tabular plain text file.
#   This differs from the usual human-readable output, but is particularly convenient for automated processing.
#
# Next, we define the location of the BLAST output file.
# Then we define variables that contain paths to: the input query sequence file, the database we are searching against, and the file containing the BLAST output.
# Finally, we generate the command to run BLASTX.
@task
def generate_blastx_command(
    datadir: str, outdir: str, query: str, db: str, blast_output: str
) -> Tuple[str, str]:
    # define paths to input and output directories
    os.makedirs(outdir, exist_ok=True)  # create output directory if it doesn't exist

    # define paths to input and output files
    query = os.path.join(datadir, query)  # query sequence(s)
    db = os.path.join(datadir, db)  # BLAST database
    blastout = os.path.join(outdir, blast_output)  # BLAST output

    # create command-line for BLASTX
    cmd_blastx = NcbiblastxCommandline(query=query, out=blastout, outfmt=6, db=db)

    return str(cmd_blastx), blastout


# %%
# A ``ShellTask`` is useful to run commands on the shell.
# In our example, we use ``ShellTask`` to run the BLASTX command.
#
# ``{inputs.x}`` is a placeholder for the command.
# ``{outputs.output}`` is a placeholder for the output ``FlyteFile`` to record the standard output and error.
#
# .. note::
#    The new input/output placeholder syntax of ``ShellTask`` is available starting Flytekit 0.30.0b8+.
blastx_on_shell = ShellTask(
    name="blastx",
    debug=True,
    script="{inputs.x} > {outputs.output}",
    inputs=kwtypes(x=str),
    output_locs=[
        OutputLocation(var="output", var_type=FlyteFile, location="stdout.txt")
    ],
)
# %%
# If the command works, then there should be no output or error.

# %%
# Next, we define a task to load the BLASTX output. The task returns a pandas DataFrame and a plot.
# ``blastout`` contains the path to the BLAST output file.

BLASTXOutput = NamedTuple("blastx_output", result=pd.DataFrame, plot=PNGImageFile)


@task
def blastx_output(blastout: str) -> BLASTXOutput:
    # Read BLASTX output
    result = pd.read_csv(blastout, sep="\t", header=None)

    # Define column headers
    headers = [
        "query",
        "subject",
        "pc_identity",
        "aln_length",
        "mismatches",
        "gaps_opened",
        "query_start",
        "query_end",
        "subject_start",
        "subject_end",
        "e_value",
        "bitscore",
    ]

    # Assign headers
    result.columns = headers

    # Create a scatterplot
    result.plot.scatter("pc_identity", "e_value")
    plt.title("E value vs %identity")
    plot = "plot.png"
    plt.savefig(plot)

    return BLASTXOutput(result=result.head(), plot=plot)

# %%
# To ascertain whether the BLASTX standard error and output is empty, we write a task.
# If empty, then the BLASTX run was successful, else, the run failed.
@task
def is_batchx_success(stdout: FlyteFile) -> bool:
    if open(stdout).read():
        return False
    else:
        return True


# %%
# Next, we define a workflow to call the aforementioned tasks.
# We use :ref:`conditional <sphx_glr_auto_core_control_flow_run_conditions.py>` to check if the BLASTX command succeeded.
@workflow
def blast_wf(
    datadir: str = "data/kitasatospora",
    outdir: str = "output",
    query: str = "k_sp_CB01950_penicillin.fasta",
    db: str = "kitasatospora_proteins.faa",
    blast_output: str = "AMK19_00175_blastx_kitasatospora.tab",
) -> BLASTXOutput:
    cmd, blastout = generate_blastx_command(
        datadir=datadir, outdir=outdir, query=query, db=db, blast_output=blast_output
    )
    stdout = blastx_on_shell(x=cmd)
    result = is_batchx_success(stdout=stdout)
    result, plot = (
        conditional("blastx_output")
        .if_(result.is_true())
        .then(blastx_output(blastout=blastout))
        .else_()
        .fail("BLASTX failed")
    )
    return BLASTXOutput(result=result, plot=plot)


# %%
# Finally, we can run the workflow locally.
if __name__ == "__main__":
    print("Running BLASTX...")
    print(f"BLASTX result: {blast_wf()}")
