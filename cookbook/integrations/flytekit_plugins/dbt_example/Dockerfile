FROM python:3.8-slim-buster

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

RUN apt-get update && apt-get install -y build-essential git postgresql-client libpq-dev

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY dbt_example/requirements.txt /root/
RUN pip install -r /root/requirements.txt
# psycopg2-binary is a dependency of the dbt-postgres adapter, but that doesn't work on mac M1s.
# As per https://github.com/psycopg/psycopg2/issues/1360, we install psycopg to circumvent this.
RUN pip uninstall -y psycopg2-binary && pip install psycopg2

# Copy the makefile targets to expose on the container. This makes it easier to register.
COPY in_container.mk /root/Makefile
COPY dbt_example/sandbox.config /root

# Copy the actual code
COPY dbt_example/ /root/dbt_example/

# Copy dbt-specific files
COPY dbt_example/profiles.yml /root/dbt-profiles/
RUN git clone https://github.com/dbt-labs/jaffle_shop.git

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag

ENV FLYTE_SDK_LOGGING_LEVEL 10
