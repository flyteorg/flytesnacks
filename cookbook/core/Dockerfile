FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# This is necessary for opencv to work
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev ffmpeg build-essential

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli

# Install gcloud for GCP
RUN apt-get install curl --assume-yes

RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY core/requirements.txt /root
RUN pip install -r /root/requirements.txt

# Create non-root user for entrypoint into container
RUN useradd -m nonroot

# Copy the makefile targets to expose on the container. This makes it easier to register
COPY --chown=nonroot:nonroot in_container.mk /home/nonroot/Makefile
COPY --chown=nonroot:nonroot core/sandbox.config /home/nonroot

# Copy the actual code
COPY --chown=nonroot:nonroot core /home/nonroot/core

USER nonroot
WORKDIR /home/nonroot
ENV PYTHONPATH /home/nonroot

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
