"""
.. _deployment-fast-registration:

#################
Fast Registration
#################

.. NOTE::

To avoid having to wait for an image build to test out simple code changes to your Flyte workflows and reduce iteration cycles to mere seconds, read on below.

Caveats
=======
Fast registration only works when you're testing out code changes. If you need to update your container by installing a dependency or modifying a Dockerfile, you **must** use the conventional method of committing your changes and rebuilding a container image.


Steps to Follow
===============

1. Make some code changes. 
2. Save your files.
3. Clear and create (or, clear or create) the directory used to store your serialized code archive:

.. code-block:: bash 

   mkdir _pb_output || true
   rm -f _pb_output/*.tar.gz 

4. Assume a role that has the write access to the intermittent directory you'll use to store fast registration code distributions.
5. Using a Python environment with Flytekit installed, fast-register your changes:

.. code-block:: bash 

   pyflyte -c sandbox.config --pkgs recipes serialize --in-container-config-path /root/sandbox.config \
       --local-source-root <path to your code> --image <older/existing docker image here> fast workflows -f _pb_output/

Or, from within your container:

.. code-block:: bash

    pyflyte --config /root/sandbox.config serialize fast workflows -f _pb_output/ 

    The command to fast-register the changes is:

    .. code-block:: bash

        pyflyte --pkgs core package --image <your-base-image> --source /code/myproject/ --config /code/myproject/development.config --fast --force

6. Next, fast-register your serialized files. You'll note the overlap with the existing register command (auth role and output location) but with a new flag pointing to an additional distribution dir. This must be writable from the role you assume and readable from the role your Flytepropeller assumes.

.. code-block:: bash

    flytectl register files _pb_output/* -p flytetester -d development --version ${VERSION}  \
       --k8sServiceAccount ${FLYTE_AUTH_KUBERNETES_SERVICE_ACCOUNT} --outputLocationPrefix ${FLYTE_AUTH_RAW_OUTPUT_DATA_PREFIX}

7. Open the Flyte UI and launch the latest version of your workflow (under the domain you fast-registered above). It should run with your new code!

"""
