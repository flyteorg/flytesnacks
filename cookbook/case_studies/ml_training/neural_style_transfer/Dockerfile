FROM ubuntu:focal
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y make build-essential libssl-dev curl python3.9 python3.9-venv

# Virtual environment
RUN python3.9 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install the AWS cli for AWS support
RUN pip3 install awscli

# Install gcloud for GCP
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

# Install Python dependencies
COPY neural_style_transfer/requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the actual code
COPY neural_style_transfer/ /root/neural_style_transfer/

# Copy the makefile targets to expose on the container. This makes it easier to register.
COPY in_container.mk /root/Makefile
COPY neural_style_transfer/sandbox.config /root

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
