# FROM python:3.8-slim-buster
  #RUN apt-get update && apt-get install -y curl less vim
  #ENV TMPDIR /large_tmp_volume
  #RUN pip install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.4.6/tested_requirements/requirements_38.reqs
  #RUN pip install snowflake-connector-python[pandas]==2.4.6

FROM python:3.8-buster

WORKDIR /root

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli

RUN pip3 install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.4.6/tested_requirements/requirements_38.reqs
# Install Python dependencies
COPY snowflake/requirements.txt /root/.
RUN pip3 install -r /root/requirements.txt

# Copy the makefile targets to expose on the container. This makes it easier to register.
COPY in_container.mk /root/Makefile
COPY snowflake/sandbox.config /root

# Copy the actual code
COPY snowflake/ /root/snowflake/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
