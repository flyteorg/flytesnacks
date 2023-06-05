FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytesnacks

ARG DOCKER_USERNAME
ARG DOCKER_PASSWORD

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

# This is necessary for opencv to work
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev ffmpeg build-essential curl
RUN curl -sSL https://get.docker.com/ | sh

WORKDIR /root

# Install Python dependencies
RUN pip install flytekit flytekitplugins-envd scikit-learn
RUN pip freeze

# Copy the makefile targets to expose on the container. This makes it easier to register
COPY image_spec_example/in_container.mk /root/Makefile
COPY image_spec_example/sandbox.config /root

# Copy the actual code
COPY ./image_spec_example /root/image_spec_example

RUN echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin ghcr.io

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
