FROM databricksruntime/standard:12.2-LTS
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytesnacks

ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /databricks/driver
ENV PATH="/databricks/python3/bin:$PATH"
USER 0

RUN sudo apt-get update && sudo apt-get install -y make build-essential libssl-dev git

# Install Python dependencies
COPY ./requirements.txt /databricks/driver/requirements.txt
RUN /databricks/python3/bin/pip install -r /databricks/driver/requirements.txt

WORKDIR /databricks/driver

# Copy the actual code
COPY . /databricks/driver/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows and launch plans.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
