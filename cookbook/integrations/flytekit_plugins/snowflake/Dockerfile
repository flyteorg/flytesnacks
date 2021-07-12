FROM python:3.8-slim-buster

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli
RUN apt-get update && apt-get install -y libssl-dev libffi-dev

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

RUN pip install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.4.6/tested_requirements/requirements_38.reqs
# Install Python dependencies
COPY snowflake/requirements.txt /root/.
RUN pip install -r /root/requirements.txt

# Copy the makefile targets to expose on the container. This makes it easier to register.
COPY in_container.mk /root/Makefile
COPY snowflake/sandbox.config /root

# Copy the actual code
COPY snowflake/ /root/dolt/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
