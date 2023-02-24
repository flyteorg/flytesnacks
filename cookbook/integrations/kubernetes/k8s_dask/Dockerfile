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
    && apt-get install -y \
    	build-essential \
    	curl \
    	git \
    	libssl-dev \
    	make \
    	python3-pip \
    	python3.8 \
    	python3.8-venv \
    && rm -rf /var/lib/apt/lists/* \
    && :

# Install AWS CLI to run on AWS (for GCS install GSutil). This will be removed
# in future versions to make it completely portable
RUN pip3 install awscli

WORKDIR /opt
RUN curl https://sdk.cloud.google.com > install.sh
RUN bash /opt/install.sh --install-dir=/opt
ENV PATH $PATH:/opt/google-cloud-sdk/bin
WORKDIR /root

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

RUN pip3 install wheel

# Install Python dependencies
COPY k8s_dask/requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the makefile targets to expose on the container. This makes it easier to register.
# Delete this after we update CI
COPY in_container.mk /root/Makefile

# Delete this after we update CI to not serialize inside the container
COPY k8s_dask/sandbox.config /root

# Copy the actual code
COPY k8s_dask/ /root/k8s_dask

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
