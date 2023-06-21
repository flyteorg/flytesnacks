FROM databricksruntime/standard:11.3-LTS
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytesnacks
# To build this dockerfile, run "make docker_build".

ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /databricks/driver
ENV PATH="/databricks/python3/bin:$PATH"
USER 0

RUN sudo apt-get update && sudo apt-get install -y make build-essential libssl-dev git

# Install custom package
RUN /databricks/python3/bin/pip install awscli
WORKDIR /opt
RUN curl https://sdk.cloud.google.com > install.sh
RUN bash /opt/install.sh --install-dir=/opt

# Install Python dependencies
COPY databricks/requirements.txt /databricks/driver/requirements.txt
RUN /databricks/python3/bin/pip install -r /databricks/driver/requirements.txt

WORKDIR /databricks/driver
# Copy the makefile targets to expose on the container. This makes it easier to register.
# Delete this after we update CI
COPY databricks/in_container.mk /databricks/driver/Makefile

# Delete this after we update CI to not serialize inside the container
COPY databricks/sandbox.config /databricks/driver

# Copy the actual code
COPY databricks/ /databricks/driver/databricks/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
