# ######################
# NOTE: For CI/CD only #
########################
FROM ubuntu:focal
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

# Install Python3 and other basics
RUN apt-get update \
	&& apt-get install -y software-properties-common \
	&& add-apt-repository ppa:ubuntu-toolchain-r/test \
	&& add-apt-repository -y ppa:deadsnakes/ppa \
	&& apt-get install -y \
	build-essential \
	curl \
	git \
	libssl-dev \
	make \
	python3-pip \
	python3.11 \
	python3.11-venv \
	&& rm -rf /var/lib/apt/lists/* \
	&& :

ENV VENV /opt/venv
# Virtual environment
RUN python3.11 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the actual code
COPY . /root/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
