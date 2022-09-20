"""
Deploying Workflows - Registration
-----------------------------------

Locally, Flytekit relies on the Python interpreter to execute tasks and workflows.
To leverage the full power of Flyte, we recommend using a deployed backend of Flyte. Flyte can be run
on any Kubernetes cluster (for example, a local cluster like `kind <https://kind.sigs.k8s.io/>`__), in a cloud environment,
or on-prem. This process of deploying your workflows to a Flyte cluster is known as ``**registration**``. It involves the
following steps:

1. Writing code, SQL etc;
2. Providing packaging in the form of Docker images for code when needed. In some cases packaging isn't needed,
   because the code itself is portable- for example SQL, or the task references a remote service - SageMaker Builtin
   algorithms, or the code can be safely transferred over;
3. Alternatively, packaging with :ref:`deployment-fast-registration`;
4. Registering the serialized workflows and tasks.

Using remote Flyte provides:

- **Caching**: To avoid calling the same task with the same inputs (for the same version);
- **Portability**: To reference pre-registered entities under any domain or project within your workflow code;
- **Shareable executions**: To easily share links of your executions with your teammates.

Refer to the :ref:`Getting Started <flyte:getting-started>` for details on Flyte installation.

Build Your Dockerfile
^^^^^^^^^^^^^^^^^^^^^^

1. Commit your changes. Some of the steps below default to referencing the git sha.
2. Run ``pyflyte register``. This :doc:`command <flytekit:pyflyte-register>` compiles all Flyte entities and sends it to the backend as specified by your config file.
3. Build a container image that holds your code.

.. code-block:: docker
   :emphasize-lines: 1
   :linenos:

   FROM python:3.8-slim-buster
   LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

   WORKDIR /root
   ENV VENV /opt/venv
   ENV LANG C.UTF-8
   ENV LC_ALL C.UTF-8
   ENV PYTHONPATH /root

   # This is necessary for opencv to work
   RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev ffmpeg build-essential

   # Install the AWS cli separately to prevent issues with boto being written over
   RUN pip3 install awscli

   ENV VENV /opt/venv
   # Virtual environment
   RUN python3 -m venv ${VENV}
   ENV PATH="${VENV}/bin:$PATH"

   # Install Python dependencies
   COPY core/requirements.txt /root
   RUN pip install -r /root/requirements.txt

   # Copy the makefile targets to expose on the container. This makes it easier to register
   COPY in_container.mk /root/Makefile
   COPY core/sandbox.config /root

   # Copy the actual code
   COPY core /root/core

   # This tag is supplied by the build script and will be used to determine the version
   # when registering tasks, workflows, and launch plans
   ARG tag
   ENV FLYTE_INTERNAL_IMAGE $tag

.. note::
   In the above Dockerfile, ``core`` directory is considered.

Serialize Your Workflows and Tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Getting your tasks, workflows, and launch plans to run on a Flyte platform is a two-step process. **Serialization** is the first step of that process.
It produces registerable protobuf files for your tasks and templates. For every task, one protobuf file is produced which represents one TaskTemplate object.
For every workflow, one protofbuf file is produced which represents a WorkflowClosure object.

Once you've built a Docker container image with your updated code changes, you can use the ``pyflyte serialize`` command to serialize your tasks:

.. code-block::

   pyflyte -c sandbox.config --pkgs core serialize --image somedocker.com/myimage:someversion123 --local-source-root ${CURDIR} --in-container-config-path /root/sandbox.config workflows -f _pb_output/

where

- :code:`-c` specifies the path to the config definition on your machine, that is, the SDK default attributes.
- :code:`--pkgs` arg points to the packages within the directory.
- ``local-source-root`` argument specifies the root directory for the Python code that contains workflow definitions to use when the code lies outside your working directory, in out of container mode.
- ``in-container-config-path`` argument specifies the configuration where the task is present inside the container. This argument is required because ``pyflyte`` utility wouldn't know the location that the Dockerfile writes the config file to.
- :code:`--image` is a non-optional fully qualified name of the container image housing your code.


Register Your Workflows and Tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once you've serialized your workflows and tasks to proto, you'll need to register them with your deployed Flyte installation.
You can register your workflows and tasks using ``pyflyte register`` command. This command ``fast regsisters`` by default.
It compiles all your Flyte entities defined in Python, and sends these entities to the backend specified by your config file.
It can be understood as combination of ``pyflyte package`` and ``flytectl register`` commands.

.. code-block::

   pyflyte register -p project_name -d domain_name -i xyz.io/docker:latest -o output_directory -d tar_file_directory --service-account account_name --raw-data-prefix offloaded_data_location -v version

where

- :code:`-p` specifies the project to register your entities. This project itself must already be registered on your Flyte deployment.s
- :code:`-d` specifies the domain to register your entities. This domain must already be configured in your Flyte deployment.
- :code:`-i` specifies the fully qualified tag for a docker image. It is optional, and if not specified, the default image is used.
- :code:`-o` specifies the directory where the zip file (containing protobuf definitions) is written to.
- :code:`-d` specifies the directory inside the image where the tar file (containing the code) is copied to.
- :code:``-service-account`` specifies the account used when creating launch plans. It is optional.
- :code:`-v` is a unique string that identifies the version of your entities to be registered under a project and domain.

Let us also understand how the combination of the ``pyflyte package`` and ``flytectl register`` commands works.

.. code-block::

   pyflyte package -i somedocker.com/myimage:someversion123 -s root/of/package/ -o path/to/python/package/source -f -p python/interpreter/loc -d path/to/copied/code/Dockerfile

where

- :code:`-i` specifies the fully qualified tag for a docker image. It is optional, and if not specified, the default image is used.
- :code:`-s` specifies the local filesystem path to the root of the package.
- :code:`-o` specifies the filesystem path to the source of the python package from where the pkgs start.
- ``fast`` flag enables fast packaging that allows ``no container build`` deploys of flyte workflows and tasks. It needs additional configuration.
- :code:`-f` flag enables overriding the existing output files. If not specified, package exits if an output file exists.
- :code:`-p` overrides the default location of the in-container Python interpreter that is used by Flyte to load your program. Flytekit is usually installed inside this container.
- :code:`-d` specifies the filesystem path to which the code is copied within Dockerfile.

.. code-block::

   flytectl register files _pb_output/* -p flytetester -d development --version ${VERSION}  --k8sServiceAccount demo --outputLocationPrefix s3://my-s3-bucket/raw_data --config path/to/config/yaml

where

- :code:`-p` specifies the project to register your entities. This project itself must already be registered on your Flyte deployment.
- :code:`-d` specifies the domain to register your entities. This domain must already be configured in your Flyte deployment
- :code:`--version` is a unique string used to identify the version of your entities to be registered under a project and domain.
- If required, you can specify a :code:`--k8sServiceAccount` and :code:`--assumableIamRole` which your tasks will run with.


Fast Registration
^^^^^^^^^^^^^^^^^^
Re-building a new Docker container image for every code change you make is cumbersome and slow.
If you're making purely code changes that **do not** require updating your container definition, you can make use of
fast serialization and registration to speed up your iteration process and reduce the time it takes to upload new entity
versions and development code to your hosted Flyte deployment.

First, run the fast serialization target:

.. code-block::

   pyflyte --pkgs core package --image core:v1 --fast --force

Next, use ``pyflyte register`` which fast registers the target:

.. code-block::

   pyflyte register -p project_name -d domain_name --output s3://my-s3-bucket/raw_data

And just like that, you can update your code without requiring a rebuild of your container!

As fast registration serializes code from your local workstation and uploads it to the hosted flyte deployment, make sure to specify the following arguments correctly to ensure that the changes are picked up when the workflow is run.

- :code:`pyflyte` has a flag :code:`--pkgs` that specifies the code to be packaged. The `fast` flag picks up the code from the local machine and provides it for execution without building and pushing a container.
- :code:`pyflyte` also has a flag  :code:`--image` to specify the Docker image that has already been built.


Building Images
^^^^^^^^^^^^^^^
If you are iterating locally, you don't need to push your Docker image. For Docker Desktop, locally built images are available for use in its K8s cluster.

If you wish to push your image to a registry (Dockerhub, ECR, etc.) later, run:


.. code-block::

    REGISTRY=docker.io/corp make all_docker_push


.. _working_hosted_service:

Pulling Images from a Private Container Image Registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use different private container registries (`AWS ECR <https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html>`__, `Docker Hub <https://docs.docker.com/docker-hub/repos/#private-repositories>`__, `GitLab Container Registry <https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#access-an-image-from-a-private-container-registry>`__). Ensure that you have the command line tools and login information associated with the registry.
An ``imagePullSecret`` is required to pull a private image.

A general trivia while using these private registries has been discussed below.

1. Using the default service account or a new service account.

   #. Add the authorization token and name to the default/new service account.
   #. Ensure that the service account you are using for authentication has permissions to access the container registry.
   #. Add your ``imagePullSecrets`` to this `service account <https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-image-pull-secret-to-service-account>`__.
   #. Use this default/new service account to login into the private registry and pull the image.

**OR**

2. Using a private registry in Docker Hub.

   #. `Use <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`__ a custom pod template to create a pod. This template is automatically added to every ``pod`` that Flyte creates.
   #. Add your ``imagePullSecrets`` to this custom pod template.
   #. Update `FlytePropeller <https://github.com/flyteorg/flyteplugins/blob/e2971efbefd9126aca0290ddc931663605dec348/go/tasks/pluginmachinery/flytek8s/config/config.go#L157>`__ about the pod created in the previous step.
   #. FlytePropeller adds ``imagePullSecrets`` (and other customization for the pod) to the PodSpec which would look similar to this `manifest <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-pod-that-uses-your-secret>`__.
   #. The pods with their keys can log in and access the images in the private registry.

Once you set up the token to authenticate with the private registry, you can pull images from them.

"""
