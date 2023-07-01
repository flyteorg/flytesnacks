"""Custom extension to auto-generate example docs from example directory."""

import inspect
import shutil
from pathlib import Path

import jupytext
import sphinx
import sphinx_gallery
from docutils import nodes
from docutils.statemachine import StringList, string2lines
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.docutils import SphinxDirective
from sphinx_gallery import gen_gallery

__version__ = "0.0.0"


TOC_TEMPLATE = """
```{{toctree}}
:maxdepth: 1
:hidden:
{toc}
```
"""

TABLE_TEMPLATE = """
```{{list-table}}
:header-rows: 0
:widths: 100
{rows}
```
"""


class AutoExamplesTOC(SphinxDirective):
    """Custom directive to convert examples into table of contents."""

    has_content = True

    def run(self) -> list:
        return [self.parse()]

    def get_root_fp(self) -> str:
        index_fp, _ = self.get_source_info()
        index_fp = Path(index_fp)
        example_fp = []
        collect = False
        for part in index_fp.parts:
            if part == "auto_examples":
                collect = True
            if collect:
                example_fp.append(part)
        return str(Path("/".join(example_fp)).parent)

    def parse(self):
        """Parses the directive"""

        root_fp = self.get_root_fp()
        toc, rows = "", ""
        for filename in self.content:
            toc += f"\n{filename}"
            rows += f"\n* - {{fa}}`file` {{doc}}`/{root_fp}/{filename}`"

        container = nodes.container("")
        toc = inspect.cleandoc(TOC_TEMPLATE.format(toc=toc))
        table = inspect.cleandoc(TABLE_TEMPLATE.format(rows=rows))
        content = f"{toc}\n\n{table}"

        self.state.nested_parse(StringList(string2lines(content)), 0, container)
        return container


# This allows the sphinx myst parser to recognize markdown files as something
# this it can potentially execute
MYST_NOTEBOOK_METADATA = {
    "jupytext": {
        "notebook_metadata_filter": "all",
        "cell_metadata_filter": "all",
        "formats": "md:myst",
        "text_representation": {
            "extension": ".md",
            "format_name": "myst",
        },
    },
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
}


def convert_to_mdmyst(file: Path, dest_dir: Path, from_format: str):
    notebook = jupytext.read(file, fmt=from_format)
    jupytext.header.recursive_update(notebook.metadata, MYST_NOTEBOOK_METADATA)
    jupytext.write(
        notebook,
        dest_dir / f"{file.stem}.md",
        fmt="md:myst",
    )


def convert_py_example(file: Path, dest_dir: Path, app: Sphinx, config: Config):
    """
    Converts a python file in the specified auto examples directory.

    Converting sphinx-gallery format python files to .rst is only supported
    for backwards compatibility. The py:percent format conversion to myst
    markdown is the strongly encouraged format.
    """
    # converts sphinx-gallery file to rst
    try:
        # try converting sphinx-gallery py:sphinx format to rst
        gen_gallery._update_gallery_conf_builder_inited(config.sphinx_gallery_conf, str(file.parent.absolute()))
        sphinx_gallery.gen_rst.generate_file_rst(
            file.name,
            target_dir=str(dest_dir.absolute()),
            src_dir=str(file.parent.absolute()),
            gallery_conf=config.sphinx_gallery_conf,
        )
    except sphinx.errors.ExtensionError:
        # otherwise assume py:percent format, convert to myst markdown
        convert_to_mdmyst(file, dest_dir, "py:percent")


def generate_auto_examples(app, config):
    """Converts all example files into myst markdown format."""
    # copy files over to docs directory
    for source_dir in (x for x in Path(config.auto_examples_dir_root).glob("*") if x.is_dir()):
        source_dir = Path(source_dir)
        dest_dir = Path("auto_examples", *source_dir.parts[2:])
        dest_dir.mkdir(exist_ok=True, parents=True)

        # copy README.md file for root project content and table of contents
        shutil.copy(source_dir / "README.md", dest_dir / "index.md")

        # assume that the python source files are in a directory with the same
        # name as the project directory
        project_name = source_dir.name
        assert (source_dir / project_name).exists(), (
            "Python example files must be the same name as the project " f"directory name {project_name}"
        )

        for f in (x for x in source_dir.glob(f"{project_name}/*.py") if x.name != "__init__.py"):
            # converts sphinx-gallery file to rst
            convert_py_example(f, dest_dir, app, config)

        for f in (x for x in source_dir.glob(f"{project_name}/*.ipynb")):
            convert_to_mdmyst(f, dest_dir, from_format="ipynb")

        for f in (x for x in source_dir.glob(f"{project_name}/*.md")):
            convert_to_mdmyst(f, dest_dir, from_format="md")


def setup(app: Sphinx) -> dict:
    app.add_config_value("auto_examples_dir_root", None, False)
    app.add_config_value("auto_examples_dirs", None, False)
    app.connect("config-inited", generate_auto_examples, priority=500)
    app.add_directive("auto-examples-toc", AutoExamplesTOC)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
