"""
.. _repo_project_build:

Setup a Project
----------------

Prerequisites
^^^^^^^^^^^^^^^^
Make sure you have `Git <https://git-scm.com/>`__, and
`Python <https://www.python.org/downloads/>`__ >= 3.7 installed.

Start a new project / repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install Flyte's Python SDK — `Flytekit <https://pypi.org/project/flytekit/>`__
on a `virtual environment <https://docs.python.org/3/library/venv.html>`__, and
run ``pyflyte init <project_name>``, where ``<project_name>`` is the directory
that will be created containing the scaffolding for a flyte-ready project.

Feel free to use any name as your project name, however for this guide we're
going call it ``my_flyte_project``:

.. prompt:: bash (venv)$

    pip install flytekit --upgrade
    pyflyte init my_flyte_project
    cd my_flyte_project

The ``my_flyte_project`` directory comes with a sample workflow, which can be found under ``flyte/workflows/example.py``. The structure below shows the most important files and how a typical Flyte app should be laid out.

.. dropdown:: A typical Flyte app should have these files

   .. code-block:: text

       my_flyte_project
       ├── Dockerfile
       ├── docker_build_and_tag.sh
       ├── flyte
       │         ├── __init__.py
       │         └── workflows
       │             ├── __init__.py
       │             └── example.py
       └── requirements.txt

   .. note::

       Two things to note here:

       * You can use `pip-compile` to build your requirements file.
       * The Dockerfile that comes with this is not GPU ready, but is a simple Dockerfile that should work for most of your apps.

Run the Workflow Locally
^^^^^^^^^^^^^^^^^^^^^^^^

The workflow can be run locally, simply by running it as a Python script:

.. prompt:: bash (venv)$

    python flyte/workflows/example.py
   
.. note::
  
   The workflow needs to be invoked after the ``if __name__ == "__main__"``
   entrypoint at the bottom of ``flyte/workflows/example.py``.


Expected output:

.. prompt:: text

  Running my_wf() hello world

"""
