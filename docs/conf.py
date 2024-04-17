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
copyright = "2023, Flyte"
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
    "sphinx_reredirects",
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
html_js_files = ["custom.js"]

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
tags_extension = ["md"]
tags_overview_title = "Example Tags"

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

announcement = """
📢 This is the old documentation for Flyte.
Please visit the new documentation <a href="https://docs.flyte.org">here</a>.
"""

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#4300c9",
        "color-brand-content": "#4300c9",
        "color-announcement-background": "#FEE7B8",
        "color-announcement-text": "#535353",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9D68E4",
        "color-brand-content": "#9D68E4",
        "color-announcement-background": "#493100",
    },
    # custom flyteorg furo theme options
    "github_repo": "flytesnacks",
    "github_username": "flyteorg",
    "github_commit": "master",
    "docs_path": "docs",  # path to documentation source
    "announcement": announcement,
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

nb_execution_mode = "auto"
nb_execution_excludepatterns = [
    "auto_examples/**/*",
]

# myst notebook docs customization
auto_examples_dir_root = "../examples"
exclude_examples = ["advanced_composition", "basics",
                    "customizing_dependencies", "data_types_and_io",
                    "development_lifecycle", "extending",
                    "productionizing", "testing"]

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
    # "greatexpectations": ("https://docs.greatexpectations.io/docs/reference/api_reference/", None),
    "tensorflow": (
        "https://www.tensorflow.org/api_docs/python",
        "https://github.com/GPflow/tensorflow-intersphinx/raw/master/tf2_py_objects.inv",
    ),
    "whylogs": ("https://whylogs.readthedocs.io/en/latest/", None),
    "horovod": ("https://horovod.readthedocs.io/en/stable/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "feast": ("https://rtd.feast.dev/en/latest", None),
}

if int(os.environ.get("ENABLE_SPHINX_REDIRECTS", 0)):
    # Redirects to the new docs site
    redirects = {
        "auto_examples/advanced_composition/waiting_for_external_inputs.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/waiting_for_external_inputs.html",
        "auto_examples/advanced_composition/eager_workflows.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/eager_workflows.html",
        "auto_examples/advanced_composition/map_task.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/map_task.html",
        "auto_examples/advanced_composition/decorating_workflows.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/decorating_workflows.html",
        "auto_examples/advanced_composition/conditional.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/conditional.html",
        "auto_examples/advanced_composition/checkpoint.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/checkpoint.html",
        "auto_examples/advanced_composition/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/index.html",
        "auto_examples/advanced_composition/dynamic_workflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/dynamic_workflow.html",
        "auto_examples/advanced_composition/decorating_tasks.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/decorating_tasks.html",
        "auto_examples/advanced_composition/chain_entities.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/chain_entities.html",
        "auto_examples/advanced_composition/subworkflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/advanced_composition/subworkflow.html",
        "auto_examples/airflow_plugin/airflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/airflow_plugin/airflow.html",
        "auto_examples/airflow_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/airflow_plugin/index.html",
        "auto_examples/athena_plugin/athena.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/athena_plugin/athena.html",
        "auto_examples/athena_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/athena_plugin/index.html",
        "auto_examples/aws_batch_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/aws_batch_plugin/index.html",
        "auto_examples/aws_batch_plugin/batch.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/aws_batch_plugin/batch.html",
        "auto_examples/basics/imperative_workflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/imperative_workflow.html",
        "auto_examples/basics/launch_plan.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/launch_plan.html",
        "auto_examples/basics/named_outputs.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/named_outputs.html",
        "auto_examples/basics/workflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/workflow.html",
        "auto_examples/basics/documenting_workflows.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/documenting_workflows.html",
        "auto_examples/basics/hello_world.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/hello_world.html",
        "auto_examples/basics/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/index.html",
        "auto_examples/basics/task.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/task.html",
        "auto_examples/basics/shell_task.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/basics/shell_task.html",
        "auto_examples/bigquery_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/bigquery_integration/index.html",
        "auto_examples/bigquery_plugin/bigquery.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/bigquery_integration/bigquery.html",
        "auto_examples/blast/blastx_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/blast/blastx_example.html",
        "auto_examples/blast/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/blast/index.html",
        "auto_examples/customizing_dependencies/image_spec.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/customizing_dependencies/image_spec.html",
        "auto_examples/customizing_dependencies/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/customizing_dependencies/index.html",
        "auto_examples/customizing_dependencies/raw_container.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/customizing_dependencies/raw_container.html",
        "auto_examples/customizing_dependencies/multi_images.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/customizing_dependencies/multi_images.html",
        "auto_examples/data_types_and_io/pytorch_type.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/pytorch_type.html",
        "auto_examples/data_types_and_io/enum_type.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/enum_type.html",
        "auto_examples/data_types_and_io/attribute_access.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/attribute_access.html",
        "auto_examples/data_types_and_io/structured_dataset.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/structured_dataset.html",
        "auto_examples/data_types_and_io/file.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/file.html",
        "auto_examples/data_types_and_io/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/index.html",
        "auto_examples/data_types_and_io/dataclass.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/dataclass.html",
        "auto_examples/data_types_and_io/folder.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/folder.html",
        "auto_examples/data_types_and_io/pickle_type.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/data_types_and_io/pickle_type.html",
        "auto_examples/databricks_plugin/databricks_job.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/databricks_integration/databricks_job.html",
        "auto_examples/databricks_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/databricks_integration/index.html",
        "auto_examples/dbt_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/dbt_plugin/index.html",
        "auto_examples/dbt_plugin/dbt_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/dbt_plugin/dbt_example.html",
        "auto_examples/development_lifecycle/inspecting_executions.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/inspecting_executions.html",
        "auto_examples/development_lifecycle/remote_task.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/remote_task.html",
        "auto_examples/development_lifecycle/debugging_workflows_tasks.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/debugging_workflows_tasks.html",
        "auto_examples/development_lifecycle/task_cache_serialize.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/task_cache_serialize.html",
        "auto_examples/development_lifecycle/decks.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/decks.html",
        "auto_examples/development_lifecycle/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/index.html",
        "auto_examples/development_lifecycle/register_project.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/register_project.html",
        "auto_examples/development_lifecycle/decks.py": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/decks.py",
        "auto_examples/development_lifecycle/remote_launchplan.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/remote_launchplan.html",
        "auto_examples/development_lifecycle/private_images.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/private_images.html",
        "auto_examples/development_lifecycle/task_cache.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/task_cache.html",
        "auto_examples/development_lifecycle/remote_workflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/remote_workflow.html",
        "auto_examples/development_lifecycle/remote_task.py": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/remote_task.py",
        "auto_examples/development_lifecycle/agent_service.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/development_lifecycle/agent_service.html",
        "auto_examples/dolt_plugin/dolt_quickstart_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/dolt_plugin/dolt_quickstart_example.html",
        "auto_examples/dolt_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/dolt_plugin/index.html",
        "auto_examples/dolt_plugin/dolt_branch_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/dolt_plugin/dolt_branch_example.html",
        "auto_examples/duckdb_plugin/duckdb_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/duckdb_plugin/duckdb_example.html",
        "auto_examples/duckdb_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/duckdb_plugin/index.html",
        "auto_examples/exploratory_data_analysis/notebook_and_task.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/notebook_and_task.html",
        "auto_examples/exploratory_data_analysis/notebooks_as_tasks.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/notebooks_as_tasks.html",
        "auto_examples/exploratory_data_analysis/supermarket_regression_1.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/supermarket_regression_1.html",
        "auto_examples/exploratory_data_analysis/supermarket_regression.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/supermarket_regression.html",
        "auto_examples/exploratory_data_analysis/notebook.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/notebook.html",
        "auto_examples/exploratory_data_analysis/supermarket_regression_2.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/supermarket_regression_2.html",
        "auto_examples/exploratory_data_analysis/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/index.html",
        "auto_examples/exploratory_data_analysis/notebook.py": "https://docs.flyte.org/en/latest/flytesnacks/examples/exploratory_data_analysis/notebook.py",
        "auto_examples/extending/custom_types.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/extending/custom_types.html",
        "auto_examples/extending/prebuilt_container.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/extending/prebuilt_container.html",
        "auto_examples/extending/container_interface.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/extending/container_interface.html",
        "auto_examples/extending/user_container.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/extending/user_container.html",
        "auto_examples/extending/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/extending/index.html",
        "auto_examples/extending/backend_plugins.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/extending/backend_plugins.html",
        "auto_examples/feast_integration/feature_eng_tasks.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/feast_integration/feature_eng_tasks.html",
        "auto_examples/feast_integration/feast_workflow.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/feast_integration/feast_workflow.html",
        "auto_examples/feast_integration/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/feast_integration/index.html",
        "auto_examples/feast_integration/feast_flyte_remote.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/feast_integration/feast_flyte_remote.html",
        "auto_examples/flyteinteractive_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/flyteinteractive_plugin/index.html",
        "auto_examples/flyteinteractive_plugin/vscode.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/flyteinteractive_plugin/vscode.html",
        "auto_examples/forecasting_sales/keras_spark_rossmann_estimator.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/forecasting_sales/keras_spark_rossmann_estimator.html",
        "auto_examples/forecasting_sales/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/forecasting_sales/index.html",
        "auto_examples/greatexpectations_plugin/task_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/greatexpectations_plugin/task_example.html",
        "auto_examples/greatexpectations_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/greatexpectations_plugin/index.html",
        "auto_examples/greatexpectations_plugin/type_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/greatexpectations_plugin/type_example.html",
        "auto_examples/hive_plugin/hive.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/hive_plugin/hive.html",
        "auto_examples/hive_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/hive_plugin/index.html",
        "auto_examples/house_price_prediction/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/house_price_prediction/index.html",
        "auto_examples/house_price_prediction/multiregion_house_price_predictor.htmlhttps://docs.flyte.org/en/latest/": "flytesnacks/examples/house_price_prediction/multiregion_house_price_predictor.html",
        "auto_examples/house_price_prediction/house_price_predictor.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/house_price_prediction/house_price_predictor.html",
        "auto_examples/k8s_dask_plugin/dask_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_dask_plugin/dask_example.html",
        "auto_examples/k8s_dask_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_dask_plugin/index.html",
        "auto_examples/k8s_pod_plugin/pod.py": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_pod_plugin/pod.py",
        "auto_examples/k8s_pod_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_pod_plugin/index.html",
        "auto_examples/k8s_pod_plugin/pod.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_pod_plugin/pod.html",
        "auto_examples/k8s_spark_plugin/dataframe_passing.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_spark_plugin/dataframe_passing.html",
        "auto_examples/k8s_spark_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_spark_plugin/index.html",
        "auto_examples/k8s_spark_plugin/pyspark_pi.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/k8s_spark_plugin/pyspark_pi.html",
        "auto_examples/kfmpi_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/kfmpi_plugin/index.html",
        "auto_examples/kfmpi_plugin/mpi_mnist.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/kfmpi_plugin/mpi_mnist.html",
        "auto_examples/kfpytorch_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/kfpytorch_plugin/index.html",
        "auto_examples/kfpytorch_plugin/pytorch_mnist.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/kfpytorch_plugin/pytorch_mnist.html",
        "auto_examples/kftensorflow_plugin/tf_mnist.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/kftensorflow_plugin/tf_mnist.html",
        "auto_examples/kftensorflow_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/kftensorflow_plugin/index.html",
        "auto_examples/mlflow_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mlflow_plugin/index.html",
        "auto_examples/mlflow_plugin/mlflow_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mlflow_plugin/mlflow_example.html",
        "auto_examples/mmcloud_plugin/example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mmcloud_integration/example.html",
        "auto_examples/mmcloud_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mmcloud_integration/index.html",
        "auto_examples/mnist_classifier/pytorch_single_node_and_gpu.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mnist_classifier/pytorch_single_node_and_gpu.html",
        "auto_examples/mnist_classifier/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mnist_classifier/index.html",
        "auto_examples/mnist_classifier/pytorch_single_node_multi_gpu.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/mnist_classifier/pytorch_single_node_multi_gpu.html",
        "auto_examples/modin_plugin/knn_classifier.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/modin_plugin/knn_classifier.html",
        "auto_examples/modin_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/modin_plugin/index.html",
        "auto_examples/nlp_processing/word2vec_and_lda.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/nlp_processing/word2vec_and_lda.html",
        "auto_examples/nlp_processing/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/nlp_processing/index.html",
        "auto_examples/onnx_plugin/scikitlearn_onnx.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/onnx_plugin/scikitlearn_onnx.html",
        "auto_examples/onnx_plugin/pytorch_onnx.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/onnx_plugin/pytorch_onnx.html",
        "auto_examples/onnx_plugin/tensorflow_onnx.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/onnx_plugin/tensorflow_onnx.html",
        "auto_examples/onnx_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/onnx_plugin/index.html",
        "auto_examples/pandera_plugin/basic_schema_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/pandera_plugin/basic_schema_example.html",
        "auto_examples/pandera_plugin/validating_and_testing_ml_pipelines.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/pandera_plugin/validating_and_testing_ml_pipelines.html",
        "auto_examples/pandera_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/pandera_plugin/index.html",
        "auto_examples/papermill_plugin/simple.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/papermill_plugin/simple.html",
        "auto_examples/papermill_plugin/nb_simple.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/papermill_plugin/nb_simple.html",
        "auto_examples/papermill_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/papermill_plugin/index.html",
        "auto_examples/pima_diabetes/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/pima_diabetes/index.html",
        "auto_examples/pima_diabetes/diabetes.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/pima_diabetes/diabetes.html",
        "auto_examples/productionizing/workflow_labels_annotations.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/workflow_labels_annotations.html",
        "auto_examples/productionizing/lp_notifications.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/lp_notifications.html",
        "auto_examples/productionizing/configure_use_gpus.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/configure_use_gpus.html",
        "auto_examples/productionizing/lp_schedules.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/lp_schedules.html",
        "auto_examples/productionizing/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/index.html",
        "auto_examples/productionizing/use_secrets.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/use_secrets.html",
        "auto_examples/productionizing/reference_task.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/reference_task.html",
        "auto_examples/productionizing/configure_logging_links.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/configure_logging_links.html",
        "auto_examples/productionizing/reference_launch_plan.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/reference_launch_plan.html",
        "auto_examples/productionizing/customizing_resources.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/customizing_resources.html",
        "auto_examples/productionizing/spot_instances.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/productionizing/spot_instances.html",
        "auto_examples/ray_plugin/ray_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/ray_plugin/ray_example.html",
        "auto_examples/ray_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/ray_plugin/index.html",
        "auto_examples/sensor/file_sensor_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/sensor/file_sensor_example.html",
        "auto_examples/sensor/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/sensor/index.html",
        "auto_examples/snowflake_plugin/snowflake.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/snowflake_integration/snowflake.html",
        "auto_examples/snowflake_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/snowflake_integration/index.html",
        "auto_examples/sql_plugin/sql_alchemy.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/sql_plugin/sql_alchemy.html",
        "auto_examples/sql_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/sql_plugin/index.html",
        "auto_examples/sql_plugin/sqlite3_integration.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/sql_plugin/sqlite3_integration.html",
        "auto_examples/testing/mocking.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/testing/mocking.html",
        "auto_examples/testing/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/testing/index.html",
        "auto_examples/whylogs_plugin/whylogs_example.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/whylogs_plugin/whylogs_example.html",
        "auto_examples/whylogs_plugin/index.html": "https://docs.flyte.org/en/latest/flytesnacks/examples/whylogs_plugin/index.html",
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
