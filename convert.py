from pathlib import Path

import re
import jupytext
from jupytext.config import JupytextConfiguration
from rst_to_myst.mdformat_render import rst_to_myst

DELIMITER = "#" * 50

# NOTE: this requires sphinx-gallery<=0.7.0
def convert(file):
    with file.open() as f:
        lines = []
        for line in f.readlines():
            if line.startswith("# %%") or line.startswith("#%%"):
                line = DELIMITER + "\n"
            lines.append(line)

    with file.open("w") as f:
        f.writelines(lines)
        
    notebook = jupytext.read(file, fmt="py:sphinx")

    delete_cells = []
    markdown_cells = []
    for cell in notebook["cells"]:
        if cell.source == "%matplotlib inline":
            delete_cells.append(cell)
        if cell.cell_type == "markdown":
            markdown_cells.append(cell)
            if cell.metadata["cell_marker"] == '"""':
                cell.metadata.cell_marker = DELIMITER

            cell.lines_to_next_cell = 1

    # combine all markdown to preserve the header hierarchy
    all_rst = "\n\nMARKDOWN_DELIMITER\n\n".join(c.source for c in markdown_cells)
    all_myst = rst_to_myst(all_rst).text.split("\n\nMARKDOWN_DELIMITER\n\n")
    assert len(all_myst) == len(markdown_cells)
    for cell, myst in zip(markdown_cells, all_myst):
        orig_refs = []
        for line in cell.source.splitlines():
            if re.match(r"# \.\. _.*:", line.strip()):
                m = re.match(r"# \.\. _(.*):", line)
                orig_refs.append(m.group(1))
            if re.match(r"\.\. _.*:", line.strip()):
                m = re.match(r"\.\. _(.*):", line)
                orig_refs.append(m.group(1))

        mod_refs = []
        for line in myst.splitlines():
            if re.match(r"# \(.*\)\=", line.strip()):
                m = re.match(r"# \((.*)\)=", line)
                mod_refs.append(m.group(1))
            if re.match(r"\(.*\)=", line.strip()):
                m = re.match(r"\((.*)\)=", line)
                mod_refs.append(m.group(1))
        
        if orig_refs:
            if len(orig_refs) != len(mod_refs):
                import ipdb; ipdb.set_trace()
            assert len(orig_refs) == len(mod_refs)
            for oref, mref in zip(orig_refs, mod_refs):
                myst = myst.replace(f"({mref})=", f"({oref})=")

        cell.source = myst

    for cell in delete_cells:
        notebook.cells.remove(cell)

    jupytext.write(
        notebook,
        file,
        fmt="py:percent",
    )


def main():
    _dir = "./examples"
    for file in Path(_dir).rglob("*.py"):
        # only convert files 4 levels deep
        if len(file.parts) != 4:
            continue
        if file.name in {"__init__.py", "hello_world.py"}:
            continue
        print(f"converting {file}")
        convert(file)


if __name__ == "__main__":
    main()
