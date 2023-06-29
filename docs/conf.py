# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys

sys.path.insert(0, os.path.abspath("../"))
sys.path.append(os.path.abspath("./_ext"))

# -- Project information -----------------------------------------------------

project = "Flytesnacks"
copyright = "2022, Flyte"
author = "Flyte"

# The full version, including alpha/beta/rc tags
release = re.sub("^v", "", os.popen("git describe").read().strip())


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx_gallery.gen_gallery",
    "sphinx-prompt",
    "sphinx_copybutton",
    "sphinxext.remoteliteralinclude",
    "sphinx_panels",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.youtube",
    "sphinx_tabs.tabs",
    "sphinx_tags",
    "myst_nb",
    # custom extensions
    "auto_examples",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
}

copybutton_exclude = 'style[type="text/css"]'

myst_enable_extensions = ["colon_fence"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

html_static_path = ["_static"]
html_css_files = ["sphx_gallery_autogen.css", "custom.css"]

suppress_warnings = ["autosectionlabel.*"]

# generate autosummary even if no references
autosummary_generate = True

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "auto/**/*.ipynb",
    "auto/**/*.py",
    "auto/**/*.md",
    "auto_examples/**/*.ipynb",
    "auto_examples/**/*.py",
    # "auto_examples/**/*.md",
    "jupyter_execute/**",
    "README.md",
]

include_patterns = [
    "auto_examples/**/index.md",
]

# The master toctree document.
master_doc = "index"

# Tags config
tags_create_tags = True
tags_page_title = "Tag"
tags_overview_title = "All Tags"

pygments_style = "tango"
pygments_dark_style = "monokai"

html_context = {
    "home_page": "https://docs.flyte.org",
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_title = "Flyte"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#4300c9",
        "color-brand-content": "#4300c9",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9D68E4",
        "color-brand-content": "#9D68E4",
    },
    # custom flyteorg furo theme options
    "github_repo": "flytesnacks",
    "github_username": "flyteorg",
    "github_commit": "master",
    "docs_path": "docs",  # path to documentation source
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_favicon = "_static/flyte_circle_gradient_1_4x4.png"
html_logo = "_static/flyte_circle_gradient_1_4x4.png"

min_reported_time = 0

sphinx_gallery_conf = {
    "examples_dirs": [],
    "gallery_dirs": [],
    # specify the order of examples to be according to filename
    "min_reported_time": min_reported_time,
    "default_thumb_file": "_static/code-example-icon.png",
    "thumbnail_size": (350, 350),
}

nb_execution_mode = "off"
nb_execution_excludepatterns = [
    "auto_examples/**/*",
]

# myst notebook docs customization
auto_examples_dir_root = "../examples"

# intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pandera": ("https://pandera.readthedocs.io/en/stable/", None),
    "modin": ("https://modin.readthedocs.io/en/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "matplotlib": ("https://matplotlib.org", None),
    "flytekit": ("https://flyte.readthedocs.io/projects/flytekit/en/latest/", None),
    "flytekitplugins": ("https://docs.flyte.org/projects/flytekit/en/latest/", None),
    "flyte": ("https://flyte.readthedocs.io/en/latest/", None),
    # Uncomment for local development and change to your username
    # "flytekit": ("/Users/ytong/go/src/github.com/lyft/flytekit/docs/build/html", None),
    "flyteidl": ("https://docs.flyte.org/projects/flyteidl/en/latest", None),
    "flytectl": ("https://docs.flyte.org/projects/flytectl/en/latest/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "greatexpectations": ("https://legacy.docs.greatexpectations.io/en/latest", None),
    "tensorflow": (
        "https://www.tensorflow.org/api_docs/python",
        "https://github.com/GPflow/tensorflow-intersphinx/raw/master/tf2_py_objects.inv",
    ),
    "whylogs": ("https://whylogs.readthedocs.io/en/latest/", None),
    "horovod": ("https://horovod.readthedocs.io/en/stable/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "feast": ("https://rtd.feast.dev/en/latest", None),
}

# Sphinx-tabs config
# sphinx_tabs_valid_builders = ["linkcheck"]

# Sphinx-mermaid config
mermaid_output_format = "raw"
mermaid_version = "latest"
mermaid_init_js = "mermaid.initialize({startOnLoad:false});"

# Disable warnings from flytekit
os.environ["FLYTE_SDK_LOGGING_LEVEL_ROOT"] = "50"

# Disable warnings from tensorflow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
