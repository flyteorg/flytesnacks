# FROM tensorflow/tensorflow:latest-gpu
# You can disable GPU support by replacing the above line with:
FROM tensorflow/tensorflow:latest

LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Install basics
# RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
# Install Python3 and other basics
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ubuntu-toolchain-r/test \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install -y \
    build-essential \
    git \
    wget \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    libssl-dev \
    python3-pip \
    python3-wheel \
    libuv1

# Virtual environment
ENV VENV /opt/venv
RUN python3.10 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install wheel after venv is activated
RUN pip3 install wheel

# Install Python dependencies
COPY requirements.in /root
RUN pip install -r /root/requirements.in

RUN wget https://tf.novaal.de/westmere/tensorflow-2.8.0-cp310-cp310-linux_x86_64.whl && pip install tensorflow-2.8.0-cp310-cp310-linux_x86_64.whl

# Copy the actual code
COPY . /root/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
